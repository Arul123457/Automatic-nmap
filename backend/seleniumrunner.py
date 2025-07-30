from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import hashlib
import time

def run_selenium_on_targets(targets, screenshot_dir="screenshots", progress_callback=None):
    os.makedirs(screenshot_dir, exist_ok=True)
    results = []

    options = Options()
    options.headless = True
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--ignore-certificate-errors")

    driver = webdriver.Chrome(options=options)

    for target in targets:
        url = target.get("url")
        ports = target.get("ports", "")

        if not url:
            print(f"[SKIP] Missing URL: {target}")
            if progress_callback:
                progress_callback()
            continue

        screenshot_path = None
        try:
            driver.set_page_load_timeout(60)
            driver.get(url)
            time.sleep(2)

            # ⏩ Bypass SSL warning if needed
            if "privacy error" in driver.title.lower() or "your connection is not private" in driver.page_source.lower():
                try:
                    driver.find_element(By.ID, "details-button").click()
                    WebDriverWait(driver, 5).until(
                        EC.element_to_be_clickable((By.ID, "proceed-link"))
                    ).click()
                    time.sleep(2)
                except Exception as e:
                    print(f"[WARN] Couldn't auto-bypass SSL warning on {url}: {e}")

            # 🚫 Skip unreachable pages based on known error messages
            error_indicators = [
                "this site can’t be reached",
                "this page isn’t working",
                "service unavailable",
                "err_name_not_resolved",
                "err_connection_refused",
                "err_connection_timed_out"
            ]

            page_text = driver.page_source.lower()
            if any(error in page_text for error in error_indicators):
                print(f"[✘] Skipped unreachable: {url}")
            else:
                # ✅ Save screenshot
                filename = hashlib.md5(url.encode()).hexdigest() + ".png"
                screenshot_path = os.path.join(screenshot_dir, filename)
                driver.save_screenshot(screenshot_path)

                results.append({
                    "url": url,
                    "ports": ports,
                    "screenshot": screenshot_path
                })

        except Exception as e:
            print(f"[ERROR] {url}: {e}")

        if progress_callback:
            progress_callback()  # ✅ Increment after each target (including skipped)

    driver.quit()
    return results

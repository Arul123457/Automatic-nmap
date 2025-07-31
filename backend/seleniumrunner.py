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

    # ✅ Prevent Chrome popup window — silent, invisible mode
    options.add_argument("--headless=new")  # New stable headless mode
    options.add_argument("--disable-gpu")  # Prevents GPU usage for better performance in headless
    options.add_argument("--no-sandbox")  # Required for root users or Docker
    options.add_argument("--disable-dev-shm-usage")  # Fix crashes on systems with low shared memory
    options.add_argument("--disable-extensions")  # Prevents extensions from launching
    options.add_argument("--disable-infobars")  # Removes "Chrome is being controlled" bar
    options.add_argument("--disable-notifications")  # Prevent popups/notifications
    options.add_argument("--window-size=1920,1080")  # Standard full HD window size
    options.add_argument("--ignore-certificate-errors")  # Accept invalid/self-signed certs
    options.add_argument("--start-maximized")  # Prevents initial small window if not headless

    # 🛑 Optional: Turn off verbose logs
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    options.add_experimental_option("useAutomationExtension", False)

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

            if "privacy error" in driver.title.lower() or "your connection is not private" in driver.page_source.lower():
                try:
                    driver.find_element(By.ID, "details-button").click()
                    WebDriverWait(driver, 5).until(
                        EC.element_to_be_clickable((By.ID, "proceed-link"))
                    ).click()
                    time.sleep(2)
                except Exception as e:
                    print(f"[WARN] Couldn't auto-bypass SSL warning on {url}: {e}")

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
            progress_callback()

    driver.quit()
    return results

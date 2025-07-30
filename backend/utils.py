def build_possible_urls(ip, port, service):
    """
    Always try both http and https versions of the IP:port, regardless of service.
    """
    port = str(port)

    urls = [
        f"http://{ip}:{port}",
        f"https://{ip}:{port}"
    ]

    return urls


# OCR-based unreachable page detection
from PIL import Image
import pytesseract

def is_unreachable_screenshot(screenshot_path):
    try:
        image = Image.open(screenshot_path)
        text = pytesseract.image_to_string(image).lower()

        error_keywords = [
            "site can't be reached",
            "this page isn’t working",
            "err_connection_refused",
            "err_name_not_resolved",
            "err_invalid_response"
        ]

        return any(keyword in text for keyword in error_keywords)

    except Exception as e:
        print(f"[OCR Error] Failed to analyze {screenshot_path}: {e}")
        return False

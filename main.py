"""
Core Playwright automation (Slowed Down Version):
- Logs into https://www.saucedemo.com with demo credentials
- Finds a product by keyword
- Prints the product name and price (final output)
- Slowed down for visible browser actions
"""

from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError
import sys
import time

SAUCE_URL = "https://www.saucedemo.com/"
USERNAME = "standard_user"
PASSWORD = "secret_sauce"

def sleep_if_enabled(delay):
    """Helper to sleep only if delay > 0"""
    if delay > 0:
        time.sleep(delay / 1000)  # convert ms to seconds

def find_product_by_keyword(page, keyword, timeout=5000):
    """
    Searches the inventory list for a product whose name contains the keyword (case-insensitive).
    Returns (name, price, product_link_element) or None if not found.
    """
    try:
        page.wait_for_selector(".inventory_list", timeout=timeout)
    except PlaywrightTimeoutError:
        return None

    items = page.query_selector_all(".inventory_item")
    print(f"Total products found: {len(items)}")
    
    for item in items:
        name_el = item.query_selector(".inventory_item_name")
        price_el = item.query_selector(".inventory_item_price")
        
        if not name_el or not price_el:
            continue

        name = name_el.inner_text().strip()
        price = price_el.inner_text().strip()

        if keyword.lower() in name.lower():
            return (name, price, name_el)
    return None


def run_task(product_keyword, headless=True, slow_mo=0):
    """
    Run the automation and return a tuple (success: bool, message: str).
    - headless=False: show browser
    - slow_mo=1000: 1 second delay between each action
    """
    try:
        with sync_playwright() as p:
            # Slow down browser automation visibly
            browser = p.chromium.launch(headless=headless, slow_mo=slow_mo)
            context = browser.new_context()
            page = context.new_page()
            page.set_default_timeout(15000)

            print("Navigating to site...")
            page.goto(SAUCE_URL)
            sleep_if_enabled(slow_mo)


            try:
                page.wait_for_selector("#user-name", timeout=8000)
                page.wait_for_selector("#password", timeout=8000)
            except PlaywrightTimeoutError:
                return (False, "Login form did not appear on time.")

            print("Filling in credentials...")
            page.fill("#user-name", USERNAME)
            sleep_if_enabled(slow_mo)
            page.fill("#password", PASSWORD)
            sleep_if_enabled(slow_mo)
            page.click("#login-button")
            print("Logging in...")
            sleep_if_enabled(slow_mo)

            print("Checking for inventory...")
            try:
                page.wait_for_selector(".inventory_list", timeout=10000)
                print("Login successful. Inventory loaded.")
            except PlaywrightTimeoutError:
                try:
                    err = page.query_selector(".error-message-container")
                    if err:
                        return (False, f"Login failed: {err.inner_text().strip()}")
                except Exception:
                    pass
                return (False, "Login may have failed or inventory didn't load.")

            print(f"Searching for product with keyword: '{product_keyword}'...")
            found = find_product_by_keyword(page, product_keyword, timeout=8000)
            if not found:
                return (False, f'Product with keyword "{product_keyword}" not found.')

            name, price, name_element = found
            print(f"Product found: {name} — Price: {price}")
            sleep_if_enabled(slow_mo)
            name_element.click()
            
            print("Opening product details...")
            sleep_if_enabled(slow_mo)

            try:
                page.wait_for_selector(".inventory_details_name", timeout=8000)
                details_name = page.query_selector(".inventory_details_name").inner_text().strip()
                details_price = page.query_selector(".inventory_details_price").inner_text().strip()
                final_message = f'Success! Product "{details_name}" found — Price: {details_price}'
                return (True, final_message)           
            except Exception:
                final_message = f'Success! Product "{name}" found — Price: {price}'
                return (True, final_message)

    except Exception as e:
        return (False, f"Unexpected error: {e}")


if __name__ == "__main__":
    product = "red"  # default product keyword

    success, message = run_task(product_keyword=product, headless=False, slow_mo=1000)
    if success:
        print(message)
        sys.exit(0)
    else:
        print("ERROR:", message)
        sys.exit(1)

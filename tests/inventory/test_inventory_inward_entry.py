# tests/inventory/test_inventory_inward_entry.py
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from conftest import BASE_URL
from utils.ui_helpers import (
    commit_number_input,
    select_autocomplete_by_index
)
from utils.assertions import assert_no_error_message


# ===============================
# REACT SAFE INPUT (IMPORTANT FIX)
# ===============================

def force_type(driver, element, value):
    driver.execute_script("""
        const element = arguments[0];
        const value = arguments[1];

        const prototype = Object.getPrototypeOf(element);
        const valueSetter = Object.getOwnPropertyDescriptor(prototype, 'value').set;

        valueSetter.call(element, value);
        element.dispatchEvent(new Event('input', { bubbles: true }));
        element.dispatchEvent(new Event('change', { bubbles: true }));
    """, element, value)


def safe_fill(driver, wait, locator, value):
    element = wait.until(EC.element_to_be_clickable(locator))
    driver.execute_script("arguments[0].scrollIntoView({block:'center'});", element)
    element.click()
    force_type(driver, element, value)
    element.send_keys(Keys.TAB)


# ===============================
# HELPERS
# ===============================

def click_button_by_text(driver, wait, text):
    btn = wait.until(
        EC.element_to_be_clickable(
            (By.XPATH, f"//button[normalize-space()='{text}']")
        )
    )
    driver.execute_script("arguments[0].scrollIntoView({block:'center'});", btn)
    driver.execute_script("arguments[0].click();", btn)


# ===============================
# TEST
# ===============================

def test_inventory_inward_entry(driver):
    wait = WebDriverWait(driver, 20)

    # ---------------------------
    # PAGE LOAD
    # ---------------------------
    driver.get(f"{BASE_URL}inventory/inward/add")

    wait.until(lambda d: d.execute_script("return document.readyState") == "complete")
    wait.until(EC.element_to_be_clickable((By.ID, "supplier-name")))

    # ---------------------------
    # SUPPLIER INFORMATION
    # ---------------------------
    safe_fill(driver, wait, (By.ID, "supplier-name"), "ABC Suppliers")
    safe_fill(driver, wait, (By.ID, "supplier-code"), "SUP-001")
    safe_fill(driver, wait, (By.ID, "invoice-number"), f"INV-{int(time.time())}")

    # ---------------------------
    # COMPONENT DETAILS
    # ---------------------------
    click_button_by_text(driver, wait, "Add Component")

    wait.until(
        EC.presence_of_element_located(
            (By.XPATH, "//div[contains(@class,'MuiAutocomplete-inputRoot')]")
        )
    )

    select_autocomplete_by_index(wait, 1)
    select_autocomplete_by_index(wait, 2)
    select_autocomplete_by_index(wait, 3)

    qty = wait.until(
        EC.element_to_be_clickable(
            (By.XPATH, "//input[@type='number' and @min='1']")
        )
    )
    commit_number_input(driver, qty, "10")

    # ---------------------------
    # ADDITIONAL INFO
    # ---------------------------
    select_autocomplete_by_index(wait, 4)

    try:
        select_autocomplete_by_index(wait, 5)
    except RuntimeError:
        pass

    # If auto redirect happened → test success
    if "/inventory" in driver.current_url and "inward/add" not in driver.current_url:
        return

    # ---------------------------
    # REMARKS
    # ---------------------------
    safe_fill(
        driver,
        wait,
        (By.TAG_NAME, "textarea"),
        "Inventory inward automation test"
    )

    # ---------------------------
    # SUBMIT
    # ---------------------------
    driver.execute_script("document.activeElement.blur();")

    submit_btn = wait.until(
    EC.presence_of_element_located((By.XPATH, "//button[@type='submit']"))
)

    driver.execute_script("arguments[0].scrollIntoView({block:'center'});", submit_btn)
    wait.until(lambda d: submit_btn.is_enabled() and submit_btn.is_displayed())

    submit_btn.click()

# Wait for table page after submit
    wait.until(EC.presence_of_element_located((By.XPATH, "//table")))



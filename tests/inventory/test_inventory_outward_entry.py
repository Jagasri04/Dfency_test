# tests/inventory/test_inventory_outward_entry.py
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException, TimeoutException
from conftest import BASE_URL
from utils.ui_helpers import (safe_text_input, commit_number_input, select_autocomplete_by_index)
from utils.assertions import (assert_form_submitted,assert_success_redirect,assert_no_error_message)


# ===============================
# HELPERS 
# ===============================

def click_button_by_text(driver, wait, text):
    btn = wait.until(
        EC.element_to_be_clickable(
            (By.XPATH, f"//button[.//text()[normalize-space()='{text}']]")
        )
    )
    driver.execute_script("arguments[0].scrollIntoView({block:'center'});", btn)
    driver.execute_script("arguments[0].click();", btn)


# ===============================
# TEST
# ===============================

def test_inventory_outward_entry(driver):
    wait = WebDriverWait(driver, 10)

    driver.get(f"{BASE_URL}inventory/outward/add")
    wait.until(lambda d: d.execute_script("return document.readyState") == "complete")

    # ===============================
    # DESTINATION INFORMATION
    # ===============================

    # 1 → Destination Type
    select_autocomplete_by_index(wait, 1)

    # Destination Name
    safe_text_input(
        driver,
        wait.until(EC.element_to_be_clickable((By.ID, "destination-name"))),
        "Production Floor"
    )

    # ===============================
    # COMPONENT DETAILS
    # ===============================

    click_button_by_text(driver, wait, "Add Component")
    wait.until(
    EC.presence_of_element_located(
        (By.XPATH, "//div[contains(@class,'MuiAutocomplete-inputRoot')]")
    )
)

    # 2 → Component
    select_autocomplete_by_index(wait, 2)

    # Quantity
    qty = wait.until(
        EC.element_to_be_clickable(
            (By.XPATH, "//input[@type='number' and @min='1']")
        )
    )
    commit_number_input(driver, qty, "5")

    # 3 → Purpose
    select_autocomplete_by_index(wait, 3)

    # ===============================
    # TRANSPORT INFORMATION
    # ===============================

    # 4 → Transport Mode
    select_autocomplete_by_index(wait, 4)

    # ===============================
    # SUBMIT
    # ===============================

    submit = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']"))
    )
    driver.execute_script("arguments[0].scrollIntoView({block:'center'});", submit)
    driver.execute_script("arguments[0].click();", submit)
          

    assert_form_submitted(driver, wait)
    assert_no_error_message(driver)

    

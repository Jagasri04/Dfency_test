# tests/inventory/test_stock_adjustment.py
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException
from conftest import BASE_URL
from utils.ui_helpers import (safe_text_input, commit_number_input, select_autocomplete_by_index)
from utils.assertions import (assert_form_submitted,assert_success_redirect,assert_no_error_message)


# ===============================
# TEST
# ===============================

def test_stock_adjustment(driver):
    wait = WebDriverWait(driver, 10)

    driver.get(f"{BASE_URL}stock/adjust")
    wait.until(lambda d: d.execute_script("return document.readyState") == "complete")

    # ===============================
    # COMPONENT SELECTION
    # ===============================

   
    select_autocomplete_by_index(wait, 1)

    # ===============================
    # ADJUSTMENT TYPE
    # ===============================


    select_autocomplete_by_index(wait, 2)

    # ===============================
    # QUANTITY
    # ===============================

    qty = wait.until(
        EC.element_to_be_clickable((By.ID, "quantity"))
    )
    commit_number_input(driver, qty, "2")

    # ===============================
    # REASON & REMARKS
    # ===============================

    reason = wait.until(
        EC.element_to_be_clickable((By.ID, "reason"))
    )
    safe_text_input(driver, reason, "Stock correction after audit")

    # ===============================
    # SUBMIT
    # ===============================

    submit = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']"))
    )
    driver.execute_script("arguments[0].scrollIntoView({block:'center'});", submit)
    driver.execute_script("arguments[0].click();", submit)


    assert_form_submitted(driver, wait)
    assert_success_redirect(wait, "/stock")
    assert_no_error_message(driver)
   

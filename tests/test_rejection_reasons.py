# tests/test_rejection_reasons.py
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from conftest import BASE_URL
from utils.ui_helpers import safe_text_input
from utils.data_factory import unique_code, unique_name

from selenium.webdriver.common.keys import Keys

def select_mui_dropdown(driver, wait, field_id, option_text):
    # Click the MUI select (more flexible locator)
    dropdown = wait.until(
        EC.element_to_be_clickable(
            (By.XPATH, f"//*[@id='{field_id}']")
        )
    )

    driver.execute_script("arguments[0].scrollIntoView(true);", dropdown)
    driver.execute_script("arguments[0].click();", dropdown)

    # Wait for dropdown menu container (MUI renders it separately)
    wait.until(
        EC.visibility_of_element_located(
            (By.XPATH, "//ul[contains(@class,'MuiList-root')]")
        )
    )

    # Now click the option by visible text (more relaxed match)
    option = wait.until(
        EC.element_to_be_clickable(
            (By.XPATH, f"//*[contains(text(), '{option_text}')]")
        )
    )

    driver.execute_script("arguments[0].click();", option)


def test_add_rejection_reason(driver):
    wait = WebDriverWait(driver, 15)

    driver.get(f"{BASE_URL}rejection-reasons")

    # ✅ Add Reason button (already fixed)
    add_reason_btn = wait.until(
        EC.element_to_be_clickable(
            (By.XPATH, "//button[contains(., 'Add Reason')]")
        )
    )
    driver.execute_script("arguments[0].click();", add_reason_btn)

    wait.until(EC.url_contains("/rejection-reasons/add"))

    safe_text_input(
        driver,
        wait.until(EC.element_to_be_clickable((By.ID, "reason-code"))),
        unique_code("RR")
    )

    safe_text_input(
        driver,
        wait.until(EC.element_to_be_clickable((By.ID, "reason-name"))),
        unique_name("RejectReason")
    )

    select_mui_dropdown(driver,wait,"severity", "Medium")

    # ✅ FIXED CREATE BUTTON CLICK
    create_btn = wait.until(
        EC.element_to_be_clickable(
            (By.XPATH, "//button[@type='submit' and contains(., 'Create')]")
        )
    )
    driver.execute_script("arguments[0].scrollIntoView({block:'center'});", create_btn)
    driver.execute_script("arguments[0].click();", create_btn)

    wait.until(EC.url_contains("/rejection-reasons"))
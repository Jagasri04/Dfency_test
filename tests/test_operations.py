# tests/test_operations.py
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from conftest import BASE_URL
from utils.ui_helpers import safe_text_input
from utils.data_factory import unique_code, unique_name

def test_add_operation(driver):
    wait = WebDriverWait(driver, 15)

    # ===============================
    # OPERATIONS PAGE
    # ===============================
    driver.get(f"{BASE_URL}operations")

    #  FIXED ADD OPERATION BUTTON 
    add_operation_btn = wait.until(
        EC.element_to_be_clickable(
            (By.XPATH, "//button[contains(., 'Add Operation')]")
        )
    )
    driver.execute_script("arguments[0].click();", add_operation_btn)

    wait.until(EC.url_contains("/operations/add"))

    # ===============================
    # ADD OPERATION FORM
    # ===============================

    safe_text_input(
        driver,
        wait.until(EC.element_to_be_clickable((By.ID, "operation-code"))),
        unique_code("OP")
    )

    safe_text_input(
        driver,
        wait.until(EC.element_to_be_clickable((By.ID, "operation-name"))),
        unique_name("Operation")
    )

    safe_text_input(
        driver,
        wait.until(EC.element_to_be_clickable((By.ID, "running-time"))),
        "40"
    )

    safe_text_input(
        driver,
        wait.until(EC.element_to_be_clickable((By.ID, "handling-time"))),
        "5.5"
    )

    safe_text_input(
        driver,
        wait.until(EC.element_to_be_clickable((By.ID, "tools-required"))),
        "Face Mill, End Mill"
    )

    #  FIXED DESCRIPTION 
    description = wait.until(
        EC.presence_of_element_located((By.ID, "description"))
    )
    description.click()
    description.clear()
    description.send_keys("Initial material removal operation")

    # ===============================
    # SUBMIT 
    # ===============================
    create_btn = wait.until(
        EC.element_to_be_clickable(
            (By.XPATH, "//button[@type='submit' and contains(., 'Create')]")
        )
    )

    driver.execute_script("arguments[0].scrollIntoView({block:'center'});", create_btn)
    driver.execute_script("arguments[0].click();", create_btn)

    # ===============================
    # SUCCESS CHECK
    # ===============================
    wait.until(EC.url_contains("/operations"))







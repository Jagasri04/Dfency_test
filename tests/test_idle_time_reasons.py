# tests/test_idle_time_reasons.py
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from conftest import BASE_URL
from utils.ui_helpers import safe_text_input
from utils.data_factory import unique_code, unique_name


def test_add_idle_time_reason(driver):
    wait = WebDriverWait(driver, 10)

    driver.get(f"{BASE_URL}idle-time-reasons")

    #  Add Reason Button Click
    add_button = wait.until(
        EC.presence_of_element_located(
            (By.XPATH, "//button[.//text()[normalize-space()='Add Reason']]")
        )
    )

    driver.execute_script(
        "arguments[0].scrollIntoView({block:'center'});",
        add_button
    )

    wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//button[.//text()[normalize-space()='Add Reason']]")
    ))

    driver.execute_script("arguments[0].click();", add_button)
    

    wait.until(EC.url_contains("/idle-time-reasons/add"))

    safe_text_input(
        driver,
        wait.until(EC.element_to_be_clickable((By.ID, "reason-code"))),
        unique_code("IT")
    )

    safe_text_input(
        driver,
        wait.until(EC.element_to_be_clickable((By.ID, "reason-name"))),
        unique_name("IdleReason")
    )

    wait.until(
        EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']"))
    ).click()

    wait.until(EC.url_contains("/idle-time-reasons"))
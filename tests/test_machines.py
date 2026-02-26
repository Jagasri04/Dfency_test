# tests/test_machines.py
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from conftest import BASE_URL
from utils.ui_helpers import safe_text_input
from utils.data_factory import unique_code, unique_name


def select_mui_dropdown(driver, element, value):
    wait = WebDriverWait(driver, 10)

    # Scroll into view
    driver.execute_script(
        "arguments[0].scrollIntoView({block:'center'});", element
    )

    # Find hidden native input inside MUI Select
    hidden_input = driver.find_element(
        By.XPATH,
        f"//input[@name='{element.get_attribute('id')}']"
    )

    # Set value using JS and trigger change event
    driver.execute_script("""
        arguments[0].value = arguments[1];
        arguments[0].dispatchEvent(new Event('change', { bubbles: true }));
    """, hidden_input, value)


def test_add_machine(driver):
    wait = WebDriverWait(driver, 15)

    driver.get(f"{BASE_URL}machines")

    # Add Machine button
    add_machine_btn = wait.until(
        EC.presence_of_element_located(
            (By.XPATH, "//button[.//text()[normalize-space()='Add Machine']]")
        )
    )

    driver.execute_script(
        "arguments[0].scrollIntoView({block:'center'});", add_machine_btn
    )
    driver.execute_script("arguments[0].click();", add_machine_btn)

    wait.until(EC.url_contains("/machines/add"))

    # Fill Form
    safe_text_input(
        driver,
        wait.until(EC.element_to_be_clickable((By.ID, "machine-code"))),
        unique_code("MC")
    )

    safe_text_input(
        driver,
        wait.until(EC.element_to_be_clickable((By.ID, "machine-name"))),
        unique_name("Machine")
    )

    safe_text_input(
        driver,
        wait.until(EC.element_to_be_clickable((By.ID, "model"))),
        "XYZ-123"
    )

    # Select different status 
    status_dropdown = wait.until(
    EC.element_to_be_clickable((By.ID, "status"))
)

    select_mui_dropdown(driver, status_dropdown, "inactive")

    # Submit
    submit_btn = wait.until(
        EC.element_to_be_clickable((
            By.XPATH,
            "//button[@type='submit' and not(@disabled)]"
        ))
    )

    driver.execute_script("arguments[0].click();", submit_btn)

    wait.until(EC.url_contains("/machines"))
# tests/test_components.py
import os
from dotenv import load_dotenv
from utils.data_factory import unique_code, unique_name
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from conftest import BASE_URL
from utils.ui_helpers import safe_text_input


# ===============================
# ENV
# ===============================
load_dotenv()

USERNAME = os.getenv("DFENCY_USERNAME")
PASSWORD = os.getenv("DFENCY_PASSWORD")

assert USERNAME, "DFENCY_USERNAME not set in .env"
assert PASSWORD, "DFENCY_PASSWORD not set in .env"


# ===============================
# TEST
# ===============================
def test_add_component(driver):
    wait = WebDriverWait(driver, 10)

    # ===============================
    # COMPONENTS PAGE
    # ===============================
    driver.get(f"{BASE_URL}components")

    #  Add Component Button Click
    add_component_btn = wait.until(
        EC.presence_of_element_located((
            By.XPATH,
            "//button[.//text()[normalize-space()='Add Component']]"
        ))
    )

    driver.execute_script(
        "arguments[0].scrollIntoView({block:'center'});",
        add_component_btn
    )

    wait.until(EC.element_to_be_clickable((
        By.XPATH,
        "//button[.//text()[normalize-space()='Add Component']]"
    )))

    driver.execute_script("arguments[0].click();", add_component_btn)
    

    wait.until(EC.url_contains("/components/add"))

    # ===============================
    # ADD COMPONENT FORM
    # ===============================

    # Component Code
    component_code = wait.until(
        EC.element_to_be_clickable((By.ID, "component-code"))
    )
    safe_text_input(driver, component_code, unique_code("COMP"))

    # Component Name
    component_name = wait.until(
        EC.element_to_be_clickable((By.ID, "component-name"))
    )
    safe_text_input(driver, component_name, unique_name("Component"))

    # ===============================
    # SUBMIT
    # ===============================
    create_btn = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']"))
    )
    create_btn.click()

    wait.until(EC.url_contains("/components"))
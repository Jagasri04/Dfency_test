#conftest.py
import os
import pytest
from dotenv import load_dotenv

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from utils.driver_setup import get_driver

load_dotenv()

USERNAME = os.getenv("DFENCY_USERNAME")
PASSWORD = os.getenv("DFENCY_PASSWORD")

BASE_URL = os.getenv("BASE_URL")

# ===============================
# DRIVER + LOGIN (SESSION LEVEL)
# ===============================
@pytest.fixture(scope="function")
def driver():
    driver = get_driver()
    wait = WebDriverWait(driver, 20)

    driver.get(BASE_URL)

    wait.until(
        EC.visibility_of_element_located((By.NAME, "username"))
    ).send_keys(USERNAME)

    wait.until(
        EC.visibility_of_element_located((By.NAME, "password"))
    ).send_keys(PASSWORD)

    wait.until(
        EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']"))
    ).click()

    wait.until(EC.url_contains("/dashboard"))

    yield driver
    driver.quit()


# ===============================
# UNIQUE CODE GENERATOR
# ===============================

@pytest.fixture
def machine_code():
    """
    Generates unique machine codes: MCH001, MCH002, ...
    """
    if not hasattr(machine_code, "counter"):
        machine_code.counter = 1

    code = f"MCH{machine_code.counter:03d}"
    machine_code.counter += 1
    return code


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()

    if rep.when == "call" and rep.failed:
        driver = item.funcargs.get("driver")
        if driver:
            screenshot_path = f"screenshots/{item.name}.png"
            driver.save_screenshot(screenshot_path)

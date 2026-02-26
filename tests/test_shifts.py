# test_shifts.py
import os
from dotenv import load_dotenv
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from utils.data_factory import unique_code, unique_name
from utils.driver_setup import get_driver

# ===============================
# ENV
# ===============================
load_dotenv()

USERNAME = os.getenv("DFENCY_USERNAME")
PASSWORD = os.getenv("DFENCY_PASSWORD")

assert USERNAME, "DFENCY_USERNAME not set in .env"
assert PASSWORD, "DFENCY_PASSWORD not set in .env"


# ===============================
# HELPERS
# ===============================

def safe_input(driver, element, value):
    driver.execute_script(
        "arguments[0].scrollIntoView({block:'center'});", element
    )
    time.sleep(0.3)

    driver.execute_script(
        "arguments[0].dispatchEvent(new MouseEvent('dblclick',{bubbles:true}));",
        element
    )
    time.sleep(0.2)

    element.send_keys(Keys.CONTROL, "a")
    element.send_keys(Keys.DELETE)
    element.send_keys(value)
    element.send_keys(Keys.TAB)


def safe_time_input(element, value):
    element.click()
    element.send_keys(Keys.CONTROL, "a")
    element.send_keys(Keys.DELETE)
    element.send_keys(value)
    element.send_keys(Keys.TAB)


# ===============================
# TEST
# ===============================

def test_add_shift():
    driver = get_driver()
    wait = WebDriverWait(driver, 30)

    try:
        # ===============================
        # LOGIN
        # ===============================
        driver.get("https://dev.ddatatechnologies.com/dfency/")

        wait.until(
            EC.visibility_of_element_located((By.NAME, "username"))
        ).send_keys(USERNAME)

        wait.until(
            EC.visibility_of_element_located((By.NAME, "password"))
        ).send_keys(PASSWORD)

        wait.until(
            EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']"))
        ).click()

        try:
            WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, "//button[text()='OK']"))
            ).click()
        except:
            pass

        wait.until(EC.url_contains("/dashboard"))

        # ===============================
        # SHIFTS PAGE
        # ===============================
        driver.get("https://dev.ddatatechnologies.com/dfency/shifts")

        # ✅ FIXED ADD SHIFT BUTTON CLICK
        add_shift_btn = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//button[contains(., 'Add Shift')]")
            )
        )
        driver.execute_script("arguments[0].click();", add_shift_btn)

        wait.until(EC.url_contains("/shifts/add"))

        # ===============================
        # ADD SHIFT FORM
        # ===============================

        shift_code = wait.until(
            EC.element_to_be_clickable((By.ID, "shift-code"))
        )
        safe_input(driver, shift_code, unique_code("SHIFT"))

        shift_name = wait.until(
            EC.element_to_be_clickable((By.ID, "shift-name"))
        )
        safe_input(driver, shift_name, unique_name("Shift"))

        start_time = wait.until(
            EC.element_to_be_clickable((By.ID, "start-time"))
        )
        safe_time_input(start_time, "09:00")

        end_time = wait.until(
            EC.element_to_be_clickable((By.ID, "end-time"))
        )
        safe_time_input(end_time, "17:00")

        duration = wait.until(
            EC.element_to_be_clickable((By.ID, "duration-hours"))
        )
        safe_input(driver, duration, "8")

        # ===============================
        # SUBMIT
        # ===============================
        create_btn = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']"))
        )
        create_btn.click()

        wait.until(EC.url_contains("/shifts"))

    finally:
        driver.quit()





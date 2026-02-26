# test_add_employee.py
import os
import uuid
from dotenv import load_dotenv
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils.driver_setup import get_driver
from utils.data_factory import unique_code



# ENV
load_dotenv()

USERNAME = os.getenv("DFENCY_USERNAME")
PASSWORD = os.getenv("DFENCY_PASSWORD")

assert USERNAME
assert PASSWORD


def test_add_employee():
    driver = get_driver()
    wait = WebDriverWait(driver, 30)

    try:
        # LOGIN
        driver.get("https://dev.ddatatechnologies.com/dfency/")
        wait.until(EC.visibility_of_element_located((By.NAME, "username"))).send_keys(USERNAME)
        wait.until(EC.visibility_of_element_located((By.NAME, "password"))).send_keys(PASSWORD)
        wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']"))).click()

        try:
            WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, "//button[text()='OK']"))
            ).click()
        except:
            pass

        wait.until(EC.url_contains("/dashboard"))

        # ADD EMPLOYEE
        driver.get("https://dev.ddatatechnologies.com/dfency/users/add")

        # ✅ Generate unique test data (fix for full-suite failure)
        unique_id = uuid.uuid4().hex[:6]
        employee_code = unique_code("EMP")
        username = f"user{unique_id}"

        wait.until(EC.visibility_of_element_located(
            (By.NAME, "employee_code")
        )).send_keys(employee_code)

        driver.find_element(By.NAME, "username").send_keys(username)
        driver.find_element(By.NAME, "first_name").send_keys("TestUser")
        driver.find_element(By.NAME, "password").send_keys("Test@123")

        wait.until(EC.element_to_be_clickable((By.ID, "role_id"))).click()
        wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//li[normalize-space()='Operator']")
        )).click()

        wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//button[@type='submit']")
        )).click()

    finally:
        driver.quit()
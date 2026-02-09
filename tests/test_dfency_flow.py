# test_dfency_flow.py
import os
from dotenv import load_dotenv

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException
from selenium.webdriver.common.keys import Keys

from utils.driver_setup import get_driver

# ENV

load_dotenv()

USERNAME = os.getenv("DFENCY_USERNAME")
PASSWORD = os.getenv("DFENCY_PASSWORD")

assert USERNAME
assert PASSWORD

# HELPERS


def commit_number_input(driver, input_el, value):
    driver.execute_script("arguments[0].scrollIntoView({block:'center'});", input_el)
    driver.execute_script(
        "arguments[0].dispatchEvent(new MouseEvent('dblclick',{bubbles:true}));",
        input_el
    )
    input_el.send_keys(Keys.CONTROL, "a")
    input_el.send_keys(value)
    input_el.send_keys(Keys.ENTER)
    input_el.send_keys(Keys.TAB)


def select_mui_option(container, wait, label_text, option_index=1):
    for _ in range(3):
        try:
            field = wait.until(
                lambda d: container.find_element(
                    By.XPATH,
                    f".//label[contains(normalize-space(),'{label_text}')]/following-sibling::div"
                )
            )
            field.click()

            option = wait.until(
                EC.visibility_of_element_located((
                    By.XPATH,
                    f"(//li[@role='option'])[{option_index}]"
                ))
            )
            field._parent.execute_script("arguments[0].click();", option)
            return
        except StaleElementReferenceException:
            continue

    raise RuntimeError(f"Failed selecting MUI option: {label_text}")


def select_autocomplete_without_label(wait):
    """
    Robust MUI Autocomplete selector (Material / Idle Reason)
    Re-locates fresh element to avoid stale reference
    """
    for _ in range(5):
        try:
            field = wait.until(
                EC.element_to_be_clickable((
                    By.XPATH,
                    "(//div[contains(@class,'MuiAutocomplete-inputRoot')])[last()]"
                ))
            )
            field.click()

            option = wait.until(
                EC.visibility_of_element_located(
                    (By.XPATH, "(//li[@role='option'])[1]")
                )
            )
            field._parent.execute_script("arguments[0].click();", option)
            return
        except StaleElementReferenceException:
            continue

    raise RuntimeError("Failed selecting autocomplete option")


def click_add_button(driver, wait, text):
    btn = wait.until(
        EC.element_to_be_clickable(
            (By.XPATH, f"//button[.//text()[normalize-space()='{text}']]")
        )
    )
    driver.execute_script("arguments[0].scrollIntoView({block:'center'});", btn)
    driver.execute_script("arguments[0].click();", btn)


# TEST

def test_dfency_complete_flow():
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
        wait.until(EC.visibility_of_element_located((By.NAME, "employee_code"))).send_keys("EMP101")
        driver.find_element(By.NAME, "username").send_keys("emp101")
        driver.find_element(By.NAME, "first_name").send_keys("TestUser")
        driver.find_element(By.NAME, "password").send_keys("Test@123")

        wait.until(EC.element_to_be_clickable((By.ID, "role_id"))).click()
        wait.until(EC.element_to_be_clickable((By.XPATH, "//li[normalize-space()='Operator']"))).click()
        wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']"))).click()

        
        # PRODUCTION ENTRY
    
        driver.get("https://dev.ddatatechnologies.com/dfency/production/add")
        wait.until(lambda d: d.execute_script("return document.readyState") == "complete")

        page = driver.find_element(By.TAG_NAME, "body")

        select_mui_option(page, wait, "Shift")
        select_mui_option(page, wait, "Operator")
        select_mui_option(page, wait, "Machine")
        select_mui_option(page, wait, "Component")
        select_mui_option(page, wait, "Operation")

        
        # QUANTITY TRACKING
        
        commit_number_input(driver, driver.find_element(By.ID, "target-qty"), "10")
        commit_number_input(driver, driver.find_element(By.ID, "production-qty"), "10")
        commit_number_input(driver, driver.find_element(By.ID, "accepted-qty"), "10")

        
        # MATERIAL CONSUMPTION
        
        click_add_button(driver, wait, "Add Material")

        select_autocomplete_without_label(wait)

        qty_consumed = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "(//input[@type='number'])[last()]")
            )
        )
        commit_number_input(driver, qty_consumed, "2")

        
        # IDLE TIME
        
        click_add_button(driver, wait, "Add Idle Time")

        start = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "(//input[@type='time'])[1]")
            )
        )
        end = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "(//input[@type='time'])[2]")
            )
        )

        start.send_keys("10:30")
        end.send_keys("10:45")

        select_autocomplete_without_label(wait)

        
        # SUBMIT
        
        wait.until(
            EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']"))
        ).click()

    finally:
        driver.quit()



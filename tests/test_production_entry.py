# test_production_entry.py
import os
from dotenv import load_dotenv
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.keys import Keys
from conftest import BASE_URL
from utils.driver_setup import get_driver

# ENV
load_dotenv()

USERNAME = os.getenv("DFENCY_USERNAME")
PASSWORD = os.getenv("DFENCY_PASSWORD")

assert USERNAME
assert PASSWORD


# ---------------- HELPERS (UNCHANGED) ----------------

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


# ---------------- TEST ----------------

def test_production_entry():
    driver = get_driver()
    wait = WebDriverWait(driver, 30)

    try:
        # LOGIN
        driver.get(BASE_URL)
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

        # PRODUCTION ENTRY
        driver.get(f"{BASE_URL}production/add")
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

        # MATERIAL
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

# re-locate end time input 
        end = wait.until(
    EC.element_to_be_clickable(
        (By.XPATH, "(//input[@type='time'])[2]")
    )
)
        end.send_keys("10:45")
        time.sleep(1)  # Wait for any potential JS processing
        

        # SUBMIT

        if "/production/entries" in driver.current_url:
            return

# Otherwise manually submit
        current_url = driver.current_url

        submit = wait.until(
    EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']"))
)

        driver.execute_script("arguments[0].click();", submit)

        wait.until(lambda d: d.current_url != current_url)
        wait.until(EC.url_contains("/production/entries"))
        
    finally:
        driver.quit()









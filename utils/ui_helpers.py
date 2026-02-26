#ui_helpers.py
import random
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException,TimeoutException

from selenium.webdriver.common.keys import Keys

def safe_text_input(driver, element, value):
    driver.execute_script("""
        const nativeInputValueSetter = Object.getOwnPropertyDescriptor(
            window.HTMLInputElement.prototype,
            'value'
        ).set;
        nativeInputValueSetter.call(arguments[0], arguments[1]);
        arguments[0].dispatchEvent(new Event('input', { bubbles: true }));
    """, element, value)

    element.send_keys(Keys.TAB)


def commit_number_input(driver, element, value):
    driver.execute_script("""
        const nativeInputValueSetter = Object.getOwnPropertyDescriptor(
            window.HTMLInputElement.prototype,
            'value'
        ).set;
        nativeInputValueSetter.call(arguments[0], arguments[1]);
        arguments[0].dispatchEvent(new Event('input', { bubbles: true }));
    """, element, value)

    element.send_keys(Keys.TAB)
    

def select_autocomplete_by_index(wait, index, min_options=1):
    """
    Selects a RANDOM option from MUI Autocomplete (1-based field index)
    """
    for _ in range(5):
        try:
            field = wait.until(
                EC.element_to_be_clickable(
                    (By.XPATH, f"(//div[contains(@class,'MuiAutocomplete-inputRoot')])[{index}]")
                )
            )
            field.click()

            options = wait.until(
                EC.presence_of_all_elements_located(
                    (By.XPATH, "//li[@role='option']")
                )
            )

            if len(options) < min_options:
                raise AssertionError("❌ Not enough options in autocomplete")

            option = options[0]
            field._parent.execute_script("arguments[0].click();", option)
            return

        except (StaleElementReferenceException, TimeoutException):
            continue

    raise RuntimeError(f"❌ Failed selecting autocomplete index {index}")

def set_number_input(driver, wait, element_id, value):
    element = wait.until(
        EC.element_to_be_clickable((By.ID, element_id))
    )
    safe_text_input(driver, element, str(value))









# from selenium.webdriver.common.by import By
# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.common.exceptions import StaleElementReferenceException

# def select_autocomplete_by_label(driver, wait, label_text, option_index=1):
#     for _ in range(3):
#         try:
#             # Find label
#             label = wait.until(
#                 EC.presence_of_element_located((
#                     By.XPATH,
#                     f"//label[contains(normalize-space(), '{label_text}')]"
#                 ))
#             )

#             # Find autocomplete container
#             container = label.find_element(
#                 By.XPATH,
#                 "following::div[contains(@class,'MuiAutocomplete-root')][1]"
#             )

#             driver.execute_script(
#                 "arguments[0].scrollIntoView({block:'center'});",
#                 container
#             )

#             # 🔥 Click dropdown arrow button (NOT input)
#             arrow_btn = container.find_element(
#                 By.XPATH,
#                 ".//button[contains(@class,'MuiAutocomplete-popupIndicator')]"
#             )

#             driver.execute_script("arguments[0].click();", arrow_btn)

#             # Wait for options
#             wait.until(
#                 EC.presence_of_element_located((
#                     By.XPATH,
#                     "//li[@role='option']"
#                 ))
#             )

#             options = driver.find_elements(By.XPATH, "//li[@role='option']")
#             driver.execute_script(
#                 "arguments[0].click();",
#                 options[option_index - 1]
#             )

#             return

#         except StaleElementReferenceException:
#             continue

#     raise RuntimeError(f"Failed selecting: {label_text}")


# def set_number_input(driver, wait, element_id, value):
#     element = wait.until(
#         EC.element_to_be_clickable((By.ID, element_id))
#     )
#     driver.execute_script(
#         "arguments[0].scrollIntoView({block:'center'});",
#         element
#     )
#     element.clear()
#     element.send_keys(str(value))
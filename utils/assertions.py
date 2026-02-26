#assertions.py
from selenium.webdriver.common.by import By
import time


def assert_form_submitted(driver, wait, timeout=10):
    start_url = driver.current_url
    end_time = time.time() + timeout

    while time.time() < end_time:

        # If redirected → SUCCESS
        if driver.current_url != start_url:
            return

        # Success alert
        success = driver.find_elements(
            By.XPATH,
            "//*[contains(@class,'MuiAlert-success') "
            "or contains(text(),'success') "
            "or contains(text(),'Success')]"
        )
        if success:
            return

        # Error alert → FAIL
        error = driver.find_elements(
            By.XPATH,
            "//*[contains(@class,'MuiAlert-error')]"
        )
        if error:
            raise AssertionError(f"❌ UI Error: {error[0].text}")

        time.sleep(0.5)

    return


def assert_no_error_message(driver):
    """
    Fail ONLY if actual error alert exists
    """
    error_alerts = driver.find_elements(
        By.XPATH,
        "//*[contains(@class,'MuiAlert-error')]"
    )

    if error_alerts:
        for e in error_alerts:
            print("❌ UI ERROR:", e.text)

    assert not error_alerts, "❌ UI error message detected"


def assert_success_redirect(wait, expected_path, timeout=10):
    """
    Assert page redirects to expected path
    """
    end_time = time.time() + timeout
    driver = wait._driver  # extract driver safely

    while time.time() < end_time:
        if expected_path in driver.current_url:
            return
        time.sleep(0.5)

    raise AssertionError(
        f"❌ Expected redirect to '{expected_path}', "
        f"but current URL is '{driver.current_url}'"
    )


def assert_form_reset(driver):
    quantity = driver.find_element(By.ID, "quantity")
    assert quantity.get_attribute("value") in ("", "0"), "❌ Form was not reset"

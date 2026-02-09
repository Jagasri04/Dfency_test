#driver_setup.py
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager


def get_driver():
    options = Options()
    options.add_argument("--start-maximized")

    # Disable password manager & breach popup
    prefs = {
        "credentials_enable_service": False,
        "profile.password_manager_enabled": False
    }
    options.add_experimental_option("prefs", prefs)

    #For stability
    options.add_argument("--disable-notifications")
    options.add_argument("--disable-infobars")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    driver.implicitly_wait(10)
    return driver




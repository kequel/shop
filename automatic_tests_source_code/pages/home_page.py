import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class HomePage:

    SIGN_IN_BUTTON = (By.CLASS_NAME, "logowanie")

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def go_to(self):
        """Otwiera strone glowna"""

        self.driver.get("http://localhost:8080/")

    def click_sign_in(self):
        """Klika przycisk 'Zaloguj / Zarejestruj'"""

        sign_in_link = self.wait.until(EC.element_to_be_clickable(self.SIGN_IN_BUTTON))
        sign_in_link.click()

        if not self.driver.is_headless: time.sleep(1.5)
        
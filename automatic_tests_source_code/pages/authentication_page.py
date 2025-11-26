import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class AuthenticationPage:
    
    REGISTER_BUTTON = (By.ID, "guzik_nima")

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
    
    def click_register(self):
        """Klika przycisk 'Zarejestruj się', aby przejsc do formularza"""

        register_button = self.wait.until(EC.element_to_be_clickable(self.REGISTER_BUTTON))
        register_button.click()

        if not self.driver.is_headless: time.sleep(1.5)

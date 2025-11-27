import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from variables import COMPLETE_WINDOW_SLEEP_TIME


class AuthenticationPage:
    
    # Lokator przycisku 'Zarejestruj sie'
    REGISTER_BUTTON = (By.ID, "guzik_nima")

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
    
    def click_register(self):
        """Klika przycisk 'Zarejestruj sie', aby przejsc do formularza"""

        # Czekamy az przycisk 'Zarejestruj sie' sie zaladuje
        register_button = self.wait.until(EC.element_to_be_clickable(self.REGISTER_BUTTON))

        # Klikamy ten przycisk
        register_button.click()

        # Opoznienie zeby bylo widac co sie dzieje (zeby nie bylo za szybko)
        if not self.driver.is_headless: time.sleep(COMPLETE_WINDOW_SLEEP_TIME)

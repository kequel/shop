import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from variables import COMPLETE_WINDOW_SLEEP_TIME


class CartPage:
    
    # Lokator przycisku "Finalizacja zakupow"
    PROCEED_BUTTON = (By.CSS_SELECTOR, "div.checkout a.btn-primary")

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def proceed_to_checkout(self):
        """Przechodzi z podsumowania koszyka do procesu zamawiania"""
        
        button = self.wait.until(EC.element_to_be_clickable(self.PROCEED_BUTTON))
        
        # Klikamy przycisk 'Finalizacja zakupow'
        button.click()
        
        if not self.driver.is_headless: time.sleep(COMPLETE_WINDOW_SLEEP_TIME)
        
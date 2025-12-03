import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from variables import COMPLETE_WINDOW_SLEEP_TIME


class MyAccountPage:

    # Lokator kafelka "Historia i szczegoly zamowien"
    HISTORY_LINK = (By.ID, "history-link")

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def go_to_order_history(self):
        """Klika w kafelek Historii Zamowien"""
        
        link = self.wait.until(EC.element_to_be_clickable(self.HISTORY_LINK))
        
        # Klikamy w kafelek
        link.click()
        if not self.driver.is_headless: time.sleep(COMPLETE_WINDOW_SLEEP_TIME)

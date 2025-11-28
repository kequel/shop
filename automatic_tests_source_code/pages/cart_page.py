import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from variables import COMPLETE_SECTION_SLEEP_TIME, COMPLETE_WINDOW_SLEEP_TIME


class CartPage:

    # Lokator ikony koszyka
    DELETE_ICON = (By.XPATH, "//a[@class='remove-from-cart']//i[text()='delete']")

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def remove_products(self, number_of_products_to_remove):
        """Usuwa zadana liczbe pozycji z koszyka"""
        
        for i in range(number_of_products_to_remove):
            
            # Pobieramy liste wszystkich widocznych przyciskow usuwania
            try:
                delete_buttons = self.wait.until(EC.visibility_of_any_elements_located(self.DELETE_ICON))
            except:
                raise Exception("Nie znaleziono widocznych przyciskow usuwania!")
            
            if not delete_buttons: raise Exception("Brak produktow w koszyku do usuniecia!")
            
            # Usuwamy pierwszy element z gory 
            button_to_click = delete_buttons[0]
            button_to_click.click()
            if not self.driver.is_headless: time.sleep(COMPLETE_SECTION_SLEEP_TIME)
            
            # Czekamy az klikniety element zniknie ze strony 
            self.wait.until(EC.staleness_of(button_to_click))
            if not self.driver.is_headless: time.sleep(COMPLETE_SECTION_SLEEP_TIME)

        if not self.driver.is_headless: time.sleep(COMPLETE_WINDOW_SLEEP_TIME)

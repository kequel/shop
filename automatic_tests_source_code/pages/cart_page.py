import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Dodajemy URL do importów, żeby wiedzieć na jaki adres podmienić
from variables import COMPLETE_SECTION_SLEEP_TIME, COMPLETE_WINDOW_SLEEP_TIME, URL


class CartPage:

    # Lokator ikony koszyka
    DELETE_ICON = (By.XPATH, "//a[@class='remove-from-cart']//i[text()='delete']")

    # Lokator przycisku 'Zarejestruj sie'
    REGISTER_BTN = (By.CSS_SELECTOR, "div.zarejestruj_sie a")
    
    # Lokator przycisku "Finalizacja zakupow"
    CHECKOUT_BTN = (By.CSS_SELECTOR, "a#finalb")

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def remove_products(self, number_of_products_to_remove):
        """Usuwa zadana liczbe pozycji z koszyka"""
        
        for i in range(number_of_products_to_remove):
            try:
                delete_buttons = self.wait.until(EC.visibility_of_any_elements_located(self.DELETE_ICON))
            except:
                raise Exception("Nie znaleziono widocznych przyciskow usuwania!")
            
            if not delete_buttons: raise Exception("Brak produktow w koszyku do usuniecia!")
            
            button_to_click = delete_buttons[0]
            button_to_click.click()
            if hasattr(self.driver, 'is_headless') and not self.driver.is_headless: 
                time.sleep(COMPLETE_SECTION_SLEEP_TIME)
            
            self.wait.until(EC.staleness_of(button_to_click))
            if hasattr(self.driver, 'is_headless') and not self.driver.is_headless: 
                time.sleep(COMPLETE_SECTION_SLEEP_TIME)

        if hasattr(self.driver, 'is_headless') and not self.driver.is_headless: 
            time.sleep(COMPLETE_WINDOW_SLEEP_TIME)

    def click_checkout(self):
        """Klika przycisk 'Finalizacja zakupów'"""
        
        btn = self.wait.until(EC.presence_of_element_located(self.CHECKOUT_BTN))
        self.driver.execute_script("arguments[0].click();", btn)
        
        if hasattr(self.driver, 'is_headless') and not self.driver.is_headless: 
            time.sleep(COMPLETE_WINDOW_SLEEP_TIME)

    def click_register(self):
        """
        Pobiera link z przycisku, naprawia go (zły port w HTML) 
        i przechodzi do rejestracji.
        """
        
        # Szukamy przycisku
        btn = self.wait.until(EC.presence_of_element_located(self.REGISTER_BTN))

        # ROZWIAZANIE TYMCZASOWE (BUG Z PORTEM W ADRESIE POD PRZYCISKIEM "ZAREJESTRUJ SIE")
        # Pobieramy adres URL z atrybutu href (ktory jest bledny: localhost:19662)
        raw_url = btn.get_attribute("href")

        # Podmieniamy bledny port na 19665
        if "localhost:19662" in raw_url:
             target_url = raw_url.replace("https://localhost:19662", URL)

             # Zabezpieczenie na wypadek gdyby w href nie bylo https
             target_url = target_url.replace("localhost:19662", URL.replace("https://", ""))

        else:
             # Jesli link jest inny to zostawiamy jak jest
             target_url = raw_url

        # Przechodzimy pod naprawiony adres
        self.driver.get(target_url)
        
        if hasattr(self.driver, 'is_headless') and not self.driver.is_headless: 
            time.sleep(COMPLETE_WINDOW_SLEEP_TIME)
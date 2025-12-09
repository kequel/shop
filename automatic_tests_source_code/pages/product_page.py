import time

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from variables import COMPLETE_SECTION_SLEEP_TIME, INTER_SLEEP_TIME


class ProductPage:

    # Lokator przycisku ilosci produktu
    QUANTITY_INPUT = (By.CSS_SELECTOR, "#plusminus input[name='qty']")

    # Przycisk zwiekszania ilosci
    QTY_UP_BTN = (By.CSS_SELECTOR, "#plusminus .add")
    
    # Przycisk zmniejszania ilosci
    QTY_DOWN_BTN = (By.CSS_SELECTOR, "#plusminus .sub")

    # Lokator przycisku 'Dodaj do koszyka'
    ADD_TO_CART_BTN = (By.CSS_SELECTOR, "button[data-button-action='add-to-cart']")
    
    # Lokator przycisku 'Kontynuuj zakupy' w okienku modalnym po dodaniu produktu do koszyka
    MODAL_CONTINUE_BTN = (By.XPATH, "//button[contains(text(), 'Kontynuuj zakupy')]")

    # Dodatkowy lokator do sprawdzenia samego istnienia przycisku (bez czekania na klikalność)
    ADD_BTN_SELECTOR = "button[data-button-action='add-to-cart']"

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def set_quantity(self, target_quantity):
        """Ustawia ilosc klikajac w przyciski + lub -"""
        
        qty_input = self.wait.until(EC.visibility_of_element_located(self.QUANTITY_INPUT))

        # Pobieramy aktualna wartosc (zwykle 1)
        current_qty = int(qty_input.get_attribute("value"))

        # Obliczamy roznice i klikamy odpowiednia ilosc razy
        if target_quantity > current_qty:
            clicks_needed = target_quantity - current_qty
            add_btn = self.wait.until(EC.element_to_be_clickable(self.QTY_UP_BTN))
            for _ in range(clicks_needed):
                add_btn.click()
                time.sleep(INTER_SLEEP_TIME)
        elif target_quantity < current_qty:
            clicks_needed = current_qty - target_quantity
            sub_btn = self.wait.until(EC.element_to_be_clickable(self.QTY_DOWN_BTN))
            for _ in range(clicks_needed):
                sub_btn.click()
                time.sleep(INTER_SLEEP_TIME)
        
        if not self.driver.is_headless: time.sleep(COMPLETE_SECTION_SLEEP_TIME)

    def add_to_cart(self):
        """Klika przycisk dodawania do koszyka"""

        btn = self.wait.until(EC.element_to_be_clickable(self.ADD_TO_CART_BTN))
        
        # Klika przycisk 'Dodaj do koszyka'
        btn.click()
        if not self.driver.is_headless: time.sleep(COMPLETE_SECTION_SLEEP_TIME)

    def continue_shopping(self):
        """Czeka na modal i klika 'Kontynuuj zakupy'"""
        
        continue_btn = self.wait.until(EC.visibility_of_element_located(self.MODAL_CONTINUE_BTN))
        if not self.driver.is_headless: time.sleep(COMPLETE_SECTION_SLEEP_TIME)
        
        # Klikamy 'Kontynuuj zakupy'
        continue_btn.click()
        if not self.driver.is_headless: time.sleep(COMPLETE_SECTION_SLEEP_TIME)

    def is_add_to_cart_possible(self):
        """
        Sprawdza czy przycisk dodawania do koszyka jest dostepny i aktywny.
        Zwraca True jesli mozna kupic, False jesli out-of-stock.
        """
        try:
            # Szukamy elementu z malym timeoutem lub bezposrednio w DOM
            # Uzywamy find_elements zeby nie rzucalo bledu jak nie znajdzie
            btns = self.driver.find_elements(By.CSS_SELECTOR, self.ADD_BTN_SELECTOR)
            
            if len(btns) > 0:
                btn = btns[0]
                # Sprawdzamy czy przycisk jest wyswietlony i czy jest wlaczony (nie ma atrybutu disabled)
                if btn.is_displayed() and btn.is_enabled():
                    return True
            
            return False
        except:
            return False
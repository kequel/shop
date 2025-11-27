import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from variables import COMPLETE_SECTION_SLEEP_TIME, COMPLETE_WINDOW_SLEEP_TIME


class ProductPage:

    # Lokator przycisku "Dodaj do koszyka"
    ADD_TO_CART_BUTTON = (By.CSS_SELECTOR, "button.add-to-cart, .add-to-cart")
        
    # Lokator okienka potwierdzajacego dodanie produktu do koszyka
    SUCCESS_MODAL = (By.ID, "blockcart-modal") 

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def add_to_cart(self):
        """Klika przycisk 'Dodaj do koszyka'"""

        # Czekamy az przycisk sie zaladuje 
        add_btn = self.wait.until(EC.element_to_be_clickable(self.ADD_TO_CART_BUTTON))

        # Klikamy w ten przycisk
        add_btn.click()

        # Opoznienie zeby bylo widac co sie dzieje (zeby nie bylo za szybko)
        if not self.driver.is_headless: time.sleep(COMPLETE_SECTION_SLEEP_TIME)

    def is_confirmation_popup_visible(self):
        """Sprawdza czy wyskoczylo okienko potwierdzenia"""

        try:
            # Czekamy az okienko sie zaladuje
            self.wait.until(EC.visibility_of_element_located(self.SUCCESS_MODAL))

            # Opoznienie zeby bylo widac co sie dzieje (zeby nie bylo za szybko)
            if not self.driver.is_headless: time.sleep(COMPLETE_WINDOW_SLEEP_TIME)

            return True     # Jesli sie zaladowalo (potrzebne dla asercji)
        except:

            # Opoznienie zeby bylo widac co sie dzieje (zeby nie bylo za szybko)
            if not self.driver.is_headless: time.sleep(COMPLETE_WINDOW_SLEEP_TIME)
            
            return False    # Jesli sie nie zaladowalo (potrzebne dla asercji)
import random
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from variables import COMPLETE_WINDOW_SLEEP_TIME


class SearchResultsPage:
    
    # Lokator pojedynczego kafelka produktu
    PRODUCT_LIST = (By.CSS_SELECTOR, ".product-miniature, .product-item") 

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def open_random_product(self):
        """Pobiera wszystkie produkty i klika w losowy"""
        
        # Czekamy az produkty sie zaladuja
        products = self.wait.until(EC.presence_of_all_elements_located(self.PRODUCT_LIST))
        
        # Wywalanie wyjatku jesli nie ma wynikow
        if not products: raise Exception("Nie znaleziono zadnych produktow!")

        # Losowanie ktory produkt wybierzemy
        random_product = random.choice(products)

        # Klikniecie w wylosowany produkt
        random_product.click()

        # Opoznienie zeby bylo widac co sie dzieje (zeby nie bylo za szybko)
        if not self.driver.is_headless: time.sleep(COMPLETE_WINDOW_SLEEP_TIME)

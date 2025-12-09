import time
import random

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from variables import COMPLETE_WINDOW_SLEEP_TIME, COMPLETE_SECTION_SLEEP_TIME


class CategoryPage:

    # Lokator kafelkow z produktami
    PRODUCT_TILES = (By.CSS_SELECTOR, ".js-product-miniature a.product-thumbnail")

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
        self.used_product_urls = []

    def click_random_product(self):
        """Wybiera losowy produkt z listy i wchodzi w niego"""

        try:
            # Czekmy az produkty sie zaladuja
            products = self.wait.until(EC.visibility_of_any_elements_located(self.PRODUCT_TILES))
        except:
            raise Exception(f"Nie znaleziono żadnych produktów na stronie! URL: {self.driver.current_url}")
        
        # [NOWOŚĆ] Filtrowanie produktów - bierzemy tylko te, których URL nie jest na liście użytych
        available_products = []
        for product in products:
            product_url = product.get_attribute("href")
            if product_url not in self.used_product_urls:
                available_products.append(product)

        # Sprawdzamy czy zostaly jakies produkty do wyboru
        if not available_products:
            raise Exception(f"Brak unikalnych produktów do wyboru w tej kategorii! Wykorzystano już: {len(self.used_product_urls)}")

        # Wybor losowego produktu z listy dostepnych a nie wszystkich
        random_product = random.choice(available_products)
        
        # Dodajemy URL wybranego produktu do listy użytych
        self.used_product_urls.append(random_product.get_attribute("href"))

        # Scrollujemy do tego produktu
        self.driver.execute_script("arguments[0].scrollIntoView();", random_product)
        if not self.driver.is_headless: time.sleep(COMPLETE_SECTION_SLEEP_TIME)
        
        # Klikamy wybrany produkt
        random_product.click()
        if not self.driver.is_headless: time.sleep(COMPLETE_SECTION_SLEEP_TIME)

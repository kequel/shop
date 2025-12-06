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

    def click_random_product(self):
        """Wybiera losowy produkt z listy i wchodzi w niego"""

        try:
            # Czekmy az produkty sie zaladuja
            products = self.wait.until(EC.visibility_of_any_elements_located(self.PRODUCT_TILES))
        except:
            raise Exception(f"Nie znaleziono żadnych produktów na stronie! URL: {self.driver.current_url}")
        
        # Wybor losowego produktu
        random_product = random.choice(products)
        
        # Scroll do tego produktu
        self.driver.execute_script("arguments[0].scrollIntoView();", random_product)
        if not self.driver.is_headless: time.sleep(COMPLETE_SECTION_SLEEP_TIME)
        
        # Klikamy wybrany produkt
        random_product.click()
        if not self.driver.is_headless: time.sleep(COMPLETE_SECTION_SLEEP_TIME)

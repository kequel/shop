import time
import random

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from variables import COMPLETE_WINDOW_SLEEP_TIME, COMPLETE_SECTION_SLEEP_TIME, URL


class HomePage:
    
    # Lokator panelu z kategoriami
    CATEGORY_LINKS = (By.CSS_SELECTOR, "#kategorie #top-menu > li > a")

    # Lokator ikony wozka z liczba artykolow
    CART_QUANTITY = (By.CSS_SELECTOR, ".cart-products-count")

    # Lokator searchboxa
    SEARCH_INPUT = (By.NAME, "s")

    # Lokator przycisku lupy
    SEARCH_BUTTON = (By.CSS_SELECTOR, "#search_widget button[type='submit']")

    # Lokator przycisku koszyka
    CART_BUTTON = (By.CSS_SELECTOR, "#_desktop_cart a")

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def go_to(self):
        """Wchodzi na strone"""

        self.driver.get(URL)

        self.wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        if not self.driver.is_headless: time.sleep(COMPLETE_SECTION_SLEEP_TIME)

    def get_category_elements(self):
        """Zwraca liste kategorii"""
        
        return self.wait.until(EC.presence_of_all_elements_located(self.CATEGORY_LINKS))

    def go_to_random_category(self, exclude_index=None):
        """Klika w losowa kategorie"""

        categories = self.get_category_elements()
        
        # Filtrujemy zeby nie klikac w puste linki lub ukryte
        valid_categories = [cat for cat in categories if cat.is_displayed()]
        
        if not valid_categories: raise Exception("Nie znaleziono kategorii w panelu bocznym!")

        # Logika wyboru losowego indeksu (zeby sie nie powtarzal)
        indices = list(range(len(valid_categories)))
        if exclude_index is not None and exclude_index in indices:
            indices.remove(exclude_index)
            
        random_index = random.choice(indices)

        # Wylosowana kategoria
        category_to_click = valid_categories[random_index]
        
        category_name = category_to_click.text

        # Klikamy wybrana kategorie
        category_to_click.click()
        if not self.driver.is_headless: time.sleep(COMPLETE_SECTION_SLEEP_TIME)
        
        return random_index

    def get_cart_count(self):
        """Zwraca liczbe produktow w koszyku"""

        try:
            count_element = self.driver.find_element(*self.CART_QUANTITY)
            if not count_element.text:
                return 0
            return int(count_element.text)
        except:
            return 0

    def search_for_phrase(self, phrase):
        """Wpisuje fraze w wyszukiwarke i wciska Enter"""
        
        search_input = self.wait.until(EC.visibility_of_element_located(self.SEARCH_INPUT))
        
        # Klikamy zeby aktywowac
        search_input.click() 
        
        # Wyczysc zawartosc pola tekstowego
        search_input.send_keys(Keys.CONTROL, "a")
        search_input.send_keys(Keys.BACK_SPACE)
        time.sleep(COMPLETE_SECTION_SLEEP_TIME)

        # Wpisujemy fraze
        search_input.send_keys(phrase)
        if not self.driver.is_headless: time.sleep(COMPLETE_SECTION_SLEEP_TIME)

        old_url = self.driver.current_url

        # Czekamy aż przycisk będzie w drzewie DOM
        search_btn = self.wait.until(EC.presence_of_element_located(self.SEARCH_BUTTON))

        # Klikamy lupe
        self.driver.execute_script("arguments[0].click();", search_btn)

        # Czekamy az URL sie zmieni (niezaleznie czy na liste wynikow czy na produkt)
        try:
            self.wait.until(lambda d: d.current_url != old_url)
        except:
            print("URL sie nie zmienil po kliknieciu 'szukaj'.")

        if not self.driver.is_headless: time.sleep(COMPLETE_WINDOW_SLEEP_TIME)

    def go_to_cart(self):
        """Klika w ikone koszyka, aby przejsc do podsumowania"""
        
        cart_btn = self.wait.until(EC.element_to_be_clickable(self.CART_BUTTON))

        # Klikamy przycisk koszyka
        self.driver.execute_script("arguments[0].click();", cart_btn)
        if not self.driver.is_headless: time.sleep(COMPLETE_WINDOW_SLEEP_TIME)

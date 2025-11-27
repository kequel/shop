import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from variables import COMPLETE_WINDOW_SLEEP_TIME, COMPLETE_SECTION_SLEEP_TIME, URL


class HomePage:

    # Lokator przycisku logowania
    SIGN_IN_BUTTON = (By.CLASS_NAME, "logowanie")

    # Lokator search baru
    SEARCH_INPUT = (By.NAME, "s") 

    # Lokator lupy
    SEARCH_BUTTON = (By.XPATH, "//button[contains(@type, 'submit')]")

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def go_to(self):
        """Otwiera strone glowna"""

        self.driver.get(URL)

    def click_sign_in(self):
        """Klika przycisk 'Zaloguj / Zarejestruj'"""

        sign_in_link = self.wait.until(EC.element_to_be_clickable(self.SIGN_IN_BUTTON))

        # Klikamy przycisk 'Zaloguj / Zarejestruj'
        sign_in_link.click()

        if not self.driver.is_headless: time.sleep(COMPLETE_WINDOW_SLEEP_TIME)
        
    def search_for_product(self, product_name):
        """Klika pole 'Wpisz czego szukasz...', czysci je, wpisuje losowy produkt, klika lupe"""

        search_field = self.wait.until(EC.visibility_of_element_located(self.SEARCH_INPUT))

        # Czyszcimy pole 'Wpisz czego szukasz...'
        search_field.clear()

        if not self.driver.is_headless: time.sleep(COMPLETE_SECTION_SLEEP_TIME)

        # Wpisujemy tekst do tego pola (w tym wypadku ogolna nazwa produktu)
        search_field.send_keys(product_name)

        # Klikamy lupe
        search_field.submit()

        if not self.driver.is_headless: time.sleep(COMPLETE_WINDOW_SLEEP_TIME)

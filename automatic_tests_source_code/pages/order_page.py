import time
import random

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from variables import COMPLETE_SECTION_SLEEP_TIME, COMPLETE_WINDOW_SLEEP_TIME


class OrderPage:

    # Lokatory obowiazkowych pol
    ADDRESS_INPUT = (By.NAME, "address1")
    POSTCODE_INPUT = (By.NAME, "postcode")
    CITY_INPUT = (By.NAME, "city")
    
    # Lokator przycisku 'Dalej' w sekcji z adresem dostawy
    CONFIRM_ADDRESS_BTN = (By.NAME, "confirm-addresses")

    # Lokator przycisku 'Dalej' w sekcji z potwierdzeniem dostawy
    CONFIRM_DELIVERY_BTN = (By.NAME, "confirmDeliveryOption")

    # Lokator radiobuttonow z wyborem przewoznika
    DELIVERY_OPTIONS = (By.XPATH, "//input[starts-with(@id, 'delivery_option_')]/..")

    # Lokatory opcji platnosci
    PAYMENT_OPTION_PERSONALLY = (By.CSS_SELECTOR, "label[for='payment-option-1']")
    
    # Lokator obowiazkowego checkboxu
    TERMS_CHECKBOX = (By.ID, "conditions_to_approve[terms-and-conditions]")
    
    # Lokator przycisku "Zloz zamowienie"
    PLACE_ORDER_BTN = (By.CSS_SELECTOR, "#payment-confirmation button")

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def fill_address_form(self, address, postcode, city):
        """Wypelnia pola adresu i przechodzi dalej"""
        
        # Wypelnienie obowiazkowych pol adresu dostawy
        self.wait.until(EC.visibility_of_element_located(self.ADDRESS_INPUT)).send_keys(address)
        if not self.driver.is_headless: time.sleep(COMPLETE_SECTION_SLEEP_TIME)

        self.driver.find_element(*self.POSTCODE_INPUT).send_keys(postcode)
        if not self.driver.is_headless: time.sleep(COMPLETE_SECTION_SLEEP_TIME)

        self.driver.find_element(*self.CITY_INPUT).send_keys(city)
        if not self.driver.is_headless: time.sleep(COMPLETE_SECTION_SLEEP_TIME)

        # Klikamy 'Dalej
        self.driver.find_element(*self.CONFIRM_ADDRESS_BTN).click()
        if not self.driver.is_headless: time.sleep(COMPLETE_WINDOW_SLEEP_TIME)

    def confirm_delivery(self):
        """Zatwierdza domyslna metode dostawy"""
        
        # Pobieramy liste wszystkich dostepnych opcji dostawy
        delivery_options = self.wait.until(EC.presence_of_all_elements_located(self.DELIVERY_OPTIONS))
        
        if not delivery_options: raise Exception("Nie znaleziono zadnych opcji dostawy!")

        # Losujemy jedna opcje z listy
        chosen_option = random.choice(delivery_options)
        
        # Klikamy w wybrana opcje
        chosen_option.click()
        if not self.driver.is_headless: time.sleep(COMPLETE_SECTION_SLEEP_TIME)

        # Klikamy przycisk 'Dalej'
        btn = self.wait.until(EC.element_to_be_clickable(self.CONFIRM_DELIVERY_BTN))
        btn.click()
        
        if not self.driver.is_headless: time.sleep(COMPLETE_WINDOW_SLEEP_TIME)

    def choose_payment_and_order(self):
        """Wybiera platnosc, akceptuje regulamin i sklada zamowienie"""

        # Wybieramy metode platnosci 
        pay_option = self.wait.until(EC.element_to_be_clickable(self.PAYMENT_OPTION_PERSONALLY))

        # Klikamy przycisk z wybrana metoda
        pay_option.click()
        if not self.driver.is_headless: time.sleep(COMPLETE_SECTION_SLEEP_TIME)

        # Zaznaczamy checkbox regulaminu
        terms = self.driver.find_element(*self.TERMS_CHECKBOX)
        if not terms.is_selected():
            terms.click()
        if not self.driver.is_headless: time.sleep(COMPLETE_SECTION_SLEEP_TIME)

        # Klikamy 'Zloz zamowienie' 
        order_btn = self.wait.until(EC.element_to_be_clickable(self.PLACE_ORDER_BTN))
        order_btn.click()
        
        if not self.driver.is_headless: time.sleep(COMPLETE_WINDOW_SLEEP_TIME)

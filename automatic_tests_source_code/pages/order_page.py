import time
import random
import string

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from variables import COMPLETE_SECTION_SLEEP_TIME, COMPLETE_WINDOW_SLEEP_TIME


class OrderPage:
    
    # SEKCJA 1 DANE OSOBOWE

    # Lokatory pol danych uzytkownika
    FIRST_NAME_INPUT = (By.ID, "field-firstname")
    LAST_NAME_INPUT = (By.ID, "field-lastname")
    EMAIL_INPUT = (By.ID, "field-email")
    
    # Lokatory checkboxow
    CHECKBOX_PRIVACY = (By.NAME, "customer_privacy") 
    CHECKBOX_NEWSLETTER = (By.NAME, "newsletter")
    CHECKBOX_PSGDPR = (By.NAME, "psgdpr")

    # Lokator przycisku 'Dalej'
    CONTINUE_PERSONAL_BTN = (By.CSS_SELECTOR, "button[data-link-action='register-new-customer']")



    # SEKCJA 2 ADRESY

    # Lokatory pol danych dostawy
    ADDRESS_INPUT = (By.ID, "field-address1")
    POSTCODE_INPUT = (By.ID, "field-postcode")
    CITY_INPUT = (By.ID, "field-city")
    
    # Lokatory pol opcjonalnych
    COMPANY_INPUT = (By.ID, "field-company")          
    VAT_INPUT = (By.ID, "field-vat_number")          
    ADDRESS2_INPUT = (By.ID, "field-address2")       
    PHONE_INPUT = (By.ID, "field-phone")              

    # Lokator przycisku 'Dalej'
    CONTINUE_ADDRESS_BTN = (By.NAME, "confirm-addresses")



    # SEKCJA 3 SPOSOB DOSTAWY

    # Lokator opcjonalnego komentarza
    DELIVERY_COMMENT_AREA = (By.ID, "delivery_message")

    # Lokator przycisku 'Dalej'
    CONTINUE_DELIVERY_BTN = (By.NAME, "confirmDeliveryOption")



    # SEKCJA 4 PLATNOSC

    # Lokator 'Zaplac czekiem'
    PAYMENT_CHECK_RADIO = (By.ID, "payment-option-1") 
    
    # Lokator 'Zaplac przelewem'
    PAYMENT_WIRE_RADIO = (By.ID, "payment-option-2")
    
    # Lokator checkboxu
    TERMS_CHECKBOX = (By.ID, "conditions_to_approve[terms-and-conditions]")
    
    # Lokator przycisku 'Zloz zamowienie'
    PLACE_ORDER_BTN = (By.CSS_SELECTOR, "#payment-confirmation button")
    
    # Lokator potwierdzenia zamowienia
    ORDER_CONFIRMATION_TEXT = (By.ID, "content-hook_order_confirmation")



    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def fill_personal_info(self, first_name, last_name, email):
        """Wypelnia sekcje 1: Obowiazkowe checkboxy 1 i 3, losowy 2"""
        
        self.wait.until(EC.element_to_be_clickable(self.FIRST_NAME_INPUT)).click()
        
        # Imie (obowiazkowe)
        self.driver.find_element(*self.FIRST_NAME_INPUT).send_keys(first_name)
        if not self.driver.is_headless: time.sleep(COMPLETE_SECTION_SLEEP_TIME)
        
        # Nazwisko (obowiazkowe)
        self.driver.find_element(*self.LAST_NAME_INPUT).send_keys(last_name)
        if not self.driver.is_headless: time.sleep(COMPLETE_SECTION_SLEEP_TIME)

        # Mail (obowiazkowe)
        self.driver.find_element(*self.EMAIL_INPUT).send_keys(email)
        if not self.driver.is_headless: time.sleep(COMPLETE_SECTION_SLEEP_TIME)
        
        # Checkbox dane osobowe (obowiazkowe)
        self.driver.find_element(*self.CHECKBOX_PRIVACY).click()
        if not self.driver.is_headless: time.sleep(COMPLETE_SECTION_SLEEP_TIME)

        # Checkbox newsletter (opcjonalne, losowo)
        if random.choice([True, False]): 
            self.driver.find_element(*self.CHECKBOX_NEWSLETTER).click()
            if not self.driver.is_headless: time.sleep(COMPLETE_SECTION_SLEEP_TIME)

        # Checkbox polityka prywatnosci (obowiazkowe)
        self.driver.find_element(*self.CHECKBOX_PSGDPR).click()
        if not self.driver.is_headless: time.sleep(COMPLETE_SECTION_SLEEP_TIME)
        
        # Zatwierdzamy
        self.driver.find_element(*self.CONTINUE_PERSONAL_BTN).click()
        if not self.driver.is_headless: time.sleep(COMPLETE_WINDOW_SLEEP_TIME)


    def fill_address(self, address, postcode, city):
        """Wypelnia sekcje 2: Obowiazkowe zawsze, opcjonalne losowo"""
        
        self.wait.until(EC.visibility_of_element_located(self.ADDRESS_INPUT))
        
        # Firma (opcjonalne, losowe)
        if random.choice([True, False]):
            self.driver.find_element(*self.COMPANY_INPUT).send_keys("Test Company Sp. z o.o.")
            if not self.driver.is_headless: time.sleep(COMPLETE_SECTION_SLEEP_TIME)

        # NIP UE (opcjonalne, losowe)
        if random.choice([True, False]):
            random_vat = ''.join(random.choices(string.digits, k=10))
            self.driver.find_element(*self.VAT_INPUT).send_keys(random_vat)
            if not self.driver.is_headless: time.sleep(COMPLETE_SECTION_SLEEP_TIME)

        # Adres (obowiazkowe)
        self.driver.find_element(*self.ADDRESS_INPUT).send_keys(address)
        if not self.driver.is_headless: time.sleep(COMPLETE_SECTION_SLEEP_TIME)
        
        # Uzupelnienie adresu (opcjonalne, losowe)
        if random.choice([True, False]):
            self.driver.find_element(*self.ADDRESS2_INPUT).send_keys("Lok. 5")
            if not self.driver.is_headless: time.sleep(COMPLETE_SECTION_SLEEP_TIME)

        # Kod pocztowy (obowiazkowe)
        self.driver.find_element(*self.POSTCODE_INPUT).send_keys(postcode)
        if not self.driver.is_headless: time.sleep(COMPLETE_SECTION_SLEEP_TIME)

        # Miasto (obowiazkowe)
        self.driver.find_element(*self.CITY_INPUT).send_keys(city)
        if not self.driver.is_headless: time.sleep(COMPLETE_SECTION_SLEEP_TIME)

        # Telefon (opcjonalne, losowe)
        if random.choice([True, False]):
            random_phone = ''.join(random.choices(string.digits, k=9))
            self.driver.find_element(*self.PHONE_INPUT).send_keys(random_phone)
            if not self.driver.is_headless: time.sleep(COMPLETE_SECTION_SLEEP_TIME)

        # Zatwierdzamy
        self.driver.find_element(*self.CONTINUE_ADDRESS_BTN).click()
        if not self.driver.is_headless: time.sleep(COMPLETE_WINDOW_SLEEP_TIME)


    def select_delivery(self):
        """Sekcja 3: Losowo wypelnia komentarz"""
        
        self.wait.until(EC.element_to_be_clickable(self.CONTINUE_DELIVERY_BTN))
        
        # Pole tekstowe (opcjonalne, losowo)
        if random.choice([True, False]):
            comment = "Prosze o szybka wysylke."
            self.driver.find_element(*self.DELIVERY_COMMENT_AREA).send_keys(comment)
            if not self.driver.is_headless: time.sleep(COMPLETE_SECTION_SLEEP_TIME)
            
        # Zatwierdzamy
        self.driver.find_element(*self.CONTINUE_DELIVERY_BTN).click()
        if not self.driver.is_headless: time.sleep(COMPLETE_WINDOW_SLEEP_TIME)


    def select_payment_and_order(self):
        """Sekcja 4: Wybiera losowo sposob i klika zamow"""
        
        self.wait.until(EC.presence_of_element_located(self.PAYMENT_CHECK_RADIO))
        
        # Losujemy sposob platnosci
        payment_choice = random.choice(["check", "wire"])
        
        if payment_choice == "check":
            radio_elem = self.driver.find_element(*self.PAYMENT_CHECK_RADIO)
            self.driver.execute_script("arguments[0].click();", radio_elem)
        else:
            radio_elem = self.driver.find_element(*self.PAYMENT_WIRE_RADIO)
            self.driver.execute_script("arguments[0].click();", radio_elem)

        if not self.driver.is_headless: time.sleep(COMPLETE_SECTION_SLEEP_TIME)

        # Checkbox warunki (obowiazkowe)
        terms = self.driver.find_element(*self.TERMS_CHECKBOX)
        self.driver.execute_script("arguments[0].click();", terms)
        
        if not self.driver.is_headless: time.sleep(COMPLETE_SECTION_SLEEP_TIME)

        # Klikamy "Zloz zamowienie"
        place_order_btn = self.wait.until(EC.element_to_be_clickable(self.PLACE_ORDER_BTN))
        place_order_btn.click()
        
        if not self.driver.is_headless: time.sleep(COMPLETE_WINDOW_SLEEP_TIME)

    def is_order_confirmed(self):
        """Sprawdza czy wyswietlil sie komunikat o potwierdzeniu"""
        
        try:
            self.wait.until(EC.visibility_of_element_located(self.ORDER_CONFIRMATION_TEXT))
            return True
        except:
            return False

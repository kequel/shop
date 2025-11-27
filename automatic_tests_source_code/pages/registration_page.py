import time
import random 

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from variables import COMPLETE_SECTION_SLEEP_TIME

class RegistrationPage:
    
    # Pola formularza
    GENDER_MR_RADIO = (By.ID, "field-id_gender-1") 
    GENDER_MRS_RADIO = (By.ID, "field-id_gender-2") 
    FIRST_NAME_INPUT = (By.ID, "field-firstname")
    LAST_NAME_INPUT = (By.ID, "field-lastname")
    EMAIL_INPUT = (By.ID, "field-email")
    PASSWORD_INPUT = (By.ID, "field-password")
    
    # Opcjonalne checkboxy
    PARTNER_OFFERS_CHECKBOX = (By.NAME, "optin")   
    NEWSLETTER_CHECKBOX = (By.NAME, "newsletter") 

    # Wymagane checkboxy 
    CUSTOMER_PRIVACY_CHECKBOX = (By.NAME, "customer_privacy")
    PSGDPR_CHECKBOX = (By.NAME, "psgdpr")

    # Przycisk "Zapisz"
    SUBMIT_BUTTON = (By.CSS_SELECTOR, "button[data-link-action='save-customer']")

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def fill_form_and_submit(self, first_name, last_name, email, password):
        """Wypelnia caly formularz rejestracyjny i go wysyla"""
        
        # Czekamy, aż pierwszy przycisk bedzie obecny w DOM
        self.wait.until(EC.presence_of_element_located(self.GENDER_MR_RADIO))
        
        # Losowy wybor plci
        gender_options = [self.GENDER_MR_RADIO, self.GENDER_MRS_RADIO]
        selected_gender_locator = random.choice(gender_options)
        
        gender_element = self.driver.find_element(*selected_gender_locator)
        self.driver.execute_script("arguments[0].click();", gender_element)
        if not self.driver.is_headless: time.sleep(COMPLETE_SECTION_SLEEP_TIME)

        # Pola tekstowe
        self.driver.find_element(*self.FIRST_NAME_INPUT).send_keys(first_name)
        if not self.driver.is_headless: time.sleep(COMPLETE_SECTION_SLEEP_TIME)

        self.driver.find_element(*self.LAST_NAME_INPUT).send_keys(last_name)
        if not self.driver.is_headless: time.sleep(COMPLETE_SECTION_SLEEP_TIME)

        self.driver.find_element(*self.EMAIL_INPUT).send_keys(email)
        if not self.driver.is_headless: time.sleep(COMPLETE_SECTION_SLEEP_TIME)

        self.driver.find_element(*self.PASSWORD_INPUT).send_keys(password)
        if not self.driver.is_headless: time.sleep(COMPLETE_SECTION_SLEEP_TIME)

        # Losowy wybor opcjonalnych checkboxow
        
        # Oferty partnerw 
        if random.choice([True, False]):
            partner_checkbox = self.driver.find_element(*self.PARTNER_OFFERS_CHECKBOX)
            self.driver.execute_script("arguments[0].click();", partner_checkbox)
            if not self.driver.is_headless: time.sleep(COMPLETE_SECTION_SLEEP_TIME)
        
        # Newsletter
        if random.choice([True, False]):
            newsletter_checkbox = self.driver.find_element(*self.NEWSLETTER_CHECKBOX)
            self.driver.execute_script("arguments[0].click();", newsletter_checkbox)
            if not self.driver.is_headless: time.sleep(COMPLETE_SECTION_SLEEP_TIME)

        # Zaznaczanie obowiazkowych checkboxow
        
        # Przetwarzanie danych
        customer_privacy_box = self.driver.find_element(*self.CUSTOMER_PRIVACY_CHECKBOX)
        self.driver.execute_script("arguments[0].click();", customer_privacy_box)
        if not self.driver.is_headless: time.sleep(COMPLETE_SECTION_SLEEP_TIME)

        # PSGDPR
        psgdpr_checkbox = self.driver.find_element(*self.PSGDPR_CHECKBOX)
        self.driver.execute_script("arguments[0].click();", psgdpr_checkbox)
        if not self.driver.is_headless: time.sleep(COMPLETE_SECTION_SLEEP_TIME)

        # Klik "Zapisz"
        self.driver.find_element(*self.SUBMIT_BUTTON).click()
        if not self.driver.is_headless: time.sleep(COMPLETE_SECTION_SLEEP_TIME)

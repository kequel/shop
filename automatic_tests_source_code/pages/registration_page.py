import time
import random
import string

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from variables import COMPLETE_SECTION_SLEEP_TIME, COMPLETE_WINDOW_SLEEP_TIME

class RegistrationPage:

    # Lokatory pol danych uzytkownika
    GENDER_MR_RADIO = (By.CSS_SELECTOR, "label[for='field-id_gender-1']") 
    GENDER_MRS_RADIO = (By.CSS_SELECTOR, "label[for='field-id_gender-2']")
    FIRSTNAME_INPUT = (By.NAME, "firstname")
    LASTNAME_INPUT = (By.NAME, "lastname")
    EMAIL_INPUT = (By.ID, "field-email")
    PASSWORD_INPUT = (By.NAME, "password")
    BIRTHDATE_INPUT = (By.NAME, "birthday")
    
    # Lokator checkboxow
    CHECKBOXES = (By.CSS_SELECTOR, "form#customer-form input[type='checkbox']")
    
    # Przycisk zapisu
    SUBMIT_BTN = (By.CSS_SELECTOR, "button[data-link-action='save-customer']")

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def fill_form(self, first_name, last_name, email, password, birthdate):
        """Wypelnia podstawowe pola tekstowe formularza"""
        
        # Wybor plci
        genders = [self.GENDER_MR_RADIO, self.GENDER_MRS_RADIO]
        random_gender_locator = random.choice(genders)
        
        # Klikamy w wylosowaną plec
        self.wait.until(EC.element_to_be_clickable(random_gender_locator)).click()
        
        # Wypelnianie pol
        self.driver.find_element(*self.FIRSTNAME_INPUT).send_keys(first_name)
        if not self.driver.is_headless: time.sleep(COMPLETE_SECTION_SLEEP_TIME)

        self.driver.find_element(*self.LASTNAME_INPUT).send_keys(last_name)
        if not self.driver.is_headless: time.sleep(COMPLETE_SECTION_SLEEP_TIME)

        self.driver.find_element(*self.EMAIL_INPUT).send_keys(email)
        if not self.driver.is_headless: time.sleep(COMPLETE_SECTION_SLEEP_TIME)

        self.driver.find_element(*self.PASSWORD_INPUT).send_keys(password)
        if not self.driver.is_headless: time.sleep(COMPLETE_SECTION_SLEEP_TIME)

        self.driver.find_element(*self.BIRTHDATE_INPUT).send_keys(birthdate)
        if not self.driver.is_headless: time.sleep(COMPLETE_SECTION_SLEEP_TIME)
        
        if not self.driver.is_headless: time.sleep(COMPLETE_WINDOW_SLEEP_TIME)

    def toggle_checkboxes(self):
        """
        Zaznaczamy obowiazkowo: drugi i czwarty
        Zaznaczamy losowo: pierwszy i trzeci
        """

        # Pobieramy liste wszystkich checkboxow
        checkboxes = self.wait.until(EC.presence_of_all_elements_located(self.CHECKBOXES))
        
        if len(checkboxes) < 4:
            raise Exception(f"Znaleziono mniej niz 4 checkboxy ({len(checkboxes)})!")

        # Pierwszy checkbox
        if random.choice([True, False]): 
            checkboxes[0].click()
            if not self.driver.is_headless: time.sleep(COMPLETE_SECTION_SLEEP_TIME)
            
        # Drugi checkbox
        if not checkboxes[1].is_selected():
            checkboxes[1].click()
            if not self.driver.is_headless: time.sleep(COMPLETE_SECTION_SLEEP_TIME)

        # Trzeci checkbox
        if random.choice([True, False]): 
            checkboxes[2].click()
            if not self.driver.is_headless: time.sleep(COMPLETE_SECTION_SLEEP_TIME)

        # Czwarty checkbox
        if not checkboxes[3].is_selected(): 
            checkboxes[3].click()
            if not self.driver.is_headless: time.sleep(COMPLETE_SECTION_SLEEP_TIME)

        if not self.driver.is_headless: time.sleep(COMPLETE_WINDOW_SLEEP_TIME)

    def submit_form(self):
        """Wysyla formularz"""

        self.wait.until(EC.element_to_be_clickable(self.SUBMIT_BTN)).click()

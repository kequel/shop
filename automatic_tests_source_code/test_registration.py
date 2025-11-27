import time 

from pages.home_page import HomePage
from pages.authentication_page import AuthenticationPage
from pages.registration_page import RegistrationPage
from selenium.webdriver.common.by import By


def test_new_user_registration(driver):
    
    # Inicjalizacja obiektow stron
    home_page = HomePage(driver)
    auth_page = AuthenticationPage(driver)
    reg_page = RegistrationPage(driver)

    # Generowanie unikalnego emaila
    unique_email = f"test_user_{int(time.time())}@example.com"
    
    # Wejscie na strone glowna
    home_page.go_to()

    # Klikanie 'Zaloguj / Zarejestruj'
    home_page.click_sign_in()

    # Klikanie 'Zarejestruj sie' w oknie logowania
    auth_page.click_register() 
    
    # Wprowadzenie ponizszych danych do formularza
    reg_page.fill_form_and_submit(
        first_name="Test",
        last_name="Testowy",
        email=unique_email,
        password="Qwertyui123"
    )

    # Wyologowanie po zakonczeniu rejestracji
    logout_button = driver.find_element(By.CLASS_NAME, "logout")
    assert logout_button.is_displayed(), "Rejestracja nie powiodla sie, nie znaleziono przycisku wylogowania!"

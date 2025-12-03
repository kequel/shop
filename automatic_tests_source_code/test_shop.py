import time
import random
import pytest

from pages.home_page import HomePage
from pages.category_page import CategoryPage
from pages.product_page import ProductPage
from pages.cart_page import CartPage
from pages.registration_page import RegistrationPage
from pages.order_page import OrderPage
from pages.my_account_page import MyAccountPage
from pages.order_history_page import OrderHistoryPage

from variables import (
    COMPLETE_WINDOW_SLEEP_TIME, 
    PRODUCTS_TO_BUY_IN_THE_CATEGORY, 
    SEARCH_PHRASE, 
    MAX_QTY_OF_SPECIFIC_PRODUCT, 
    PRODUCTS_TO_BUY,
    PRODUCTS_TO_REMOVE
)


def test_shop(driver):
    """
    Skrypt realizujacy:

    Dodanie do koszyka 10 produktów (w różnych ilościach) z dwóch różnych kategorii,
    Wyszukanie produktu po nazwie i dodanie do koszyka losowego produktu spośród znalezionych
    Usunięcie z koszyka 3 produktów,
    Rejestrację nowego konta,
    Wykonanie zamówienia zawartości koszyka,
    Wybór metody płatności: przy odbiorze,
    Wybór jednego z dwóch przewoźników,
    Zatwierdzenie zamówienia,
    Sprawdzenie statusu zamówienia.
    Pobranie faktury VAT.
    """

    # Inicjalizacja stron
    home_page = HomePage(driver)
    category_page = CategoryPage(driver)
    product_page = ProductPage(driver)
    cart_page = CartPage(driver)
    registration_page = RegistrationPage(driver)
    order_page = OrderPage(driver)
    my_account_page = MyAccountPage(driver)
    order_history_page = OrderHistoryPage(driver)

    # Wejscie na strone glowna
    home_page.go_to()

    # =========================================================================
    # ETAP 1: Dodawanie N produktow z dwoch roznych kategorii
    # =========================================================================
    
    # >>> Kategoria pierwsza <<<

    cat_a_index = home_page.go_to_random_category()

    for i in range(PRODUCTS_TO_BUY_IN_THE_CATEGORY):
        
        # Zapamietujemy URL kategorii zeby moc tu wrocic
        current_category_url = driver.current_url

        # Wybor i klikniecie w produkt
        category_page.click_random_product()

        # Ustawienie losowej ilosci
        qty = random.randint(1, MAX_QTY_OF_SPECIFIC_PRODUCT)
        product_page.set_quantity(qty)
        
        # Dodanie do koszyka i zamkniecie okienka
        product_page.add_to_cart()
        product_page.continue_shopping()
        
        # Powrot do kategorii
        driver.get(current_category_url)
        time.sleep(COMPLETE_WINDOW_SLEEP_TIME) 



    # >>> Kategoria druga <<<
    
    # Przechodzimy do innej losowej kategorii (wykluczajac ta pierwsza)
    _ = home_page.go_to_random_category(exclude_index=cat_a_index)

    for i in range(PRODUCTS_TO_BUY_IN_THE_CATEGORY):
        
        # Zapamietujemy URL kategorii zeby moc tu wrocic
        current_category_url = driver.current_url

        # Wybor i klikniecie w produkt
        category_page.click_random_product()

        # Ustawienie losowej ilosci
        qty = random.randint(1, MAX_QTY_OF_SPECIFIC_PRODUCT)
        product_page.set_quantity(qty)
        
        # Dodanie do koszyka i zamkniecie okienka
        product_page.add_to_cart()
        product_page.continue_shopping()
        
        # Powrot do kategorii
        driver.get(current_category_url)
        time.sleep(COMPLETE_WINDOW_SLEEP_TIME)

    

    # >>> Weryfikacja posrednia <<<

    # Sprawdzamy ile mamy produktow przed etapem wyszukiwania
    items_before_search = home_page.get_cart_count()

    print(f"Liczba sztuk w koszyku po etapie kategorii: {items_before_search}")
    
    # assert items_before_search >= PRODUCTS_TO_BUY, "Za malo produktow po etapie kategorii!"



    # =========================================================================
    # ETAP 2: Wyszukanie produktu i dodanie do koszyka
    # =========================================================================

    # Wracamy na glowna
    home_page.go_to()

    # Wyszukiwanie frazy
    home_page.search_for_phrase(SEARCH_PHRASE)

    # Sprawdzamy czy w URL jest 'controller=search'
    # Jesli tak to mamy liste wynikow i trzeba wybrać losowy produkt
    if "controller=search" in driver.current_url:
        print("Znaleziono liste wynikow - wybieram losowy produkt.")
        category_page.click_random_product()
    else:
        print("Przekierowano bezposrednio na strone produktu (tylko 1 wynik). Pomijam wybor z listy.")

    # Losowa ilosc dla produktu z wyszukiwania
    search_qty = random.randint(1, MAX_QTY_OF_SPECIFIC_PRODUCT)
    product_page.set_quantity(search_qty)

    # Dodanie do koszyka
    product_page.add_to_cart()
    product_page.continue_shopping()



    # >>> Weryfikacja posrednia <<<

    # Sprawdzamy ile mamy produktow przed etapem usuniecia
    items_before_removal = home_page.get_cart_count()

    print(f"Liczba sztuk w koszyku po etapie wyszukiwania: {items_before_removal}")

    # Asercja: mielismy X produktow. Dodalismy Y (search_qty). Powinnismy miec X + Y.
    expected_count = items_before_search + search_qty
    
    # assert items_before_removal == expected_count, \
    #    f"Blad sumowania koszyka! Mielismy {items_before_search}, dodalismy {search_qty}, a w koszyku jest {items_before_removal}"



    # =========================================================================
    # ETAP 3: Usuniecie z koszyka M produktow
    # =========================================================================

    # Przejscie do koszyka
    home_page.go_to_cart()

    # Usuniecie M pozycji
    cart_page.remove_products(PRODUCTS_TO_REMOVE)

    # >>> Weryfikacja posrednia <<<

    count_after_remove = home_page.get_cart_count()

    print(f"Liczba sztuk w koszyku po etapie usuniecia: {count_after_remove}")

    # assert count_after_remove < items_before_removal, \
    #    f"Blad usuwania! Licznik nie zmalal. Bylo: {items_before_removal}, Jest: {count_after_remove}"



    # =========================================================================
    # ETAP 4: Rejestracja nowego konta
    # =========================================================================

    # Klikamy 'Zarejestruj sie' na stronie koszyka
    cart_page.click_register()

    # Generowanie danych uzytkownika
    first_name = "Test"
    last_name = "Testowy"
    password = "qwertyui123!"
    email = f"test_{int(time.time())}@test.com" 
    birthdate = "2000-01-01"

    # Wypelnienie formularza
    registration_page.fill_form(first_name, last_name, email, password, birthdate)

    # Obsluga checkboxow (2 i 4 obowiazkowe, 1 i 3 losowe)
    registration_page.toggle_checkboxes()

    # Wyslanie formularza
    registration_page.submit_form()
    
    # Oczekiwanie na przeladowanie i przekierowanie na strone glowna
    time.sleep(COMPLETE_WINDOW_SLEEP_TIME)

    # =========================================================================
    # ETAP 5: Wykonanie zamowienia
    # =========================================================================
    
    # Przejscie do koszyka
    home_page.go_to_cart()

    # Klikniecie "Finalizacja zakupow"
    cart_page.click_checkout()

    # Wypelnienie obowiazkowych pol informacji o dostawie
    order_page.fill_address_form("Testowa 1/2", "12-345", "Testowo")

    # Potwierdzenie metody dostawy
    order_page.confirm_delivery()

    # Wybor platnosci i finalizacja
    order_page.choose_payment_and_order()

    # =========================================================================
    # ETAP 6: Weryfikacja zamowienia i pobranie faktury
    # =========================================================================

    # Przejscie do panelu klienta
    home_page.go_to_my_account()

    # Przejscie do historii zamowien
    my_account_page.go_to_order_history()

    # Wejscie w szczegoly zamowienia
    order_history_page.go_to_details()

    # Powrot do listy zamowien (imie -> historia)
    home_page.go_to_my_account()
    my_account_page.go_to_order_history()

    # Pobranie faktury
    order_history_page.download_invoice()

    # Weryfikacja pliku na dysku
    order_history_page.verify_invoice_downloaded()

import time 

from pages.home_page import HomePage
from pages.search_results_page import SearchResultsPage
from pages.product_page import ProductPage
from pages.cart_page import CartPage
from pages.order_page import OrderPage


def test_full_order_execution(driver):
    
    # Inicjalizacja obiektow stron
    home_page = HomePage(driver)
    results_page = SearchResultsPage(driver)
    product_page = ProductPage(driver)
    cart_page = CartPage(driver)
    order_page = OrderPage(driver)

    # Wejscie na strone glowna
    home_page.go_to()
    
    # TODO: LOSOWA FRAZA (na podstawie jsonow???)
    SEARCHED_PRODUCT = "Dozownik Papieru" 
    home_page.search_for_product(SEARCHED_PRODUCT)

    # Wybranie losowego produktu z listy wynikow
    results_page.open_random_product()

    # Dodanie do koszyka
    product_page.add_to_cart()
    
    # Przejscie do checkoutu z poziomu okienka
    product_page.click_proceed_to_checkout()
    
    # Przejscie z koszyka do formularzy
    cart_page.proceed_to_checkout()

    # Generowanie unikalnego maila
    unique_email = f"test_user_{int(time.time())}@example.com"

    # Dane osobowe
    order_page.fill_personal_info(
        first_name="Test",
        last_name="Testowy",
        email=unique_email
    )

    # Adresy
    order_page.fill_address(
        address="Ulica Testowa, 123",
        postcode="12-345",
        city="Testowe Miasto"
    )

    # Uzupelnienie sekcji z dostawa 
    order_page.select_delivery()

    # Wybor platnosci i finalizacja
    order_page.select_payment_and_order()

    # Asercja koncowa
    assert order_page.is_order_confirmed(), "Zamowienie nie powiodlo sie - brak potwierdzenia!"
    
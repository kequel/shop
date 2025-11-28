import time
import random
import pytest

from pages.home_page import HomePage
from pages.category_page import CategoryPage
from pages.product_page import ProductPage

from variables import COMPLETE_WINDOW_SLEEP_TIME, PRODUCTS_TO_BUY_IN_THE_CATEGORY


def test_add_products_from_two_categories(driver):

    # Inicjalizacja stron
    home_page = HomePage(driver)
    category_page = CategoryPage(driver)
    product_page = ProductPage(driver)

    # Wejscie na strone
    home_page.go_to()

    # Pierwsza kategoria
    cat_a_index = home_page.go_to_random_category()

    for i in range(PRODUCTS_TO_BUY_IN_THE_CATEGORY):

        # Wejscie w losowy produkt
        category_page.click_random_product()

        # Losowa ilosc produktu
        qty = random.randint(1, 5)
        product_page.set_quantity(qty)
        
        # Dodaj do koszyka
        product_page.add_to_cart()
        
        # Obsluga okienka 
        product_page.continue_shopping()
        
        # Powrot wstecz przegladarki do kategorii
        driver.back()
        time.sleep(COMPLETE_WINDOW_SLEEP_TIME) 

    # Druga kategoria (2 produkty)

    # Przekazujemy indeks kategorii A zeby jej nie wylosowac ponownie
    _ = home_page.go_to_random_category(exclude_index=cat_a_index)

    for i in range(PRODUCTS_TO_BUY_IN_THE_CATEGORY):
        
        # Wejscie w losowy produkt
        category_page.click_random_product()

        # Losowa ilosc produktu
        qty = random.randint(1, 5)
        product_page.set_quantity(qty)
        
        # Dodaj do koszyka
        product_page.add_to_cart()

        # Obsluga okienka
        product_page.continue_shopping()
        
        # Powrot wstecz przegladarki do kategorii
        driver.back()
        time.sleep(COMPLETE_WINDOW_SLEEP_TIME)
    
    # Weryfikacja 
    cart_items_count = home_page.get_cart_count()
     
    # Asercja: skoro dodalismy 5 produktow po minimum 1 sztuce, powinno byc >= 5 sztuk
    assert cart_items_count >= 5, "Koszyk ma mniej produktow niz oczekiwano!"

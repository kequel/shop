from pages.home_page import HomePage
from pages.search_results_page import SearchResultsPage
from pages.product_page import ProductPage


def test_search_and_add_random_product(driver):
    
    # Inicjalizacja obiektow stron
    home_page = HomePage(driver)
    results_page = SearchResultsPage(driver)
    product_page = ProductPage(driver)

    # Wejscie na strone glowna
    home_page.go_to()

    # TODO: LOSOWA FRAZA (na podstawie jsonow???)
    SEARCHED_PRODUCT = "Dozownik Papieru" 
    home_page.search_for_product(SEARCHED_PRODUCT)

    # Wybranie losowego produktu z listy wynikow
    results_page.open_random_product()

    # Dodanie do koszyka
    product_page.add_to_cart()
    
    # Asercja - czy pojawiło się potwierdzenie?
    assert product_page.is_confirmation_popup_visible(), "Nie wyswietliło sie potwierdzenie dodania do koszyka!"
    
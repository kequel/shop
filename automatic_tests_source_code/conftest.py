import pytest

from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions

# >>> >>> >>> AKTYWACJA SRODOWISKA I INSTALACJA PLUGINOW <<< <<< <<<
#
# python3 -m venv venv
# source venv/bin/activate
# pip install -r requirements.txt
#
# >>> >>> >>> URUCHOMIENIE TESTOWANIA <<< <<< <<<
#
# Graficzny Chrome (DOMYSLNIE): >>> pytest
# Graficzny Firefox:            >>> pytest --browser=firefox
#
# Headless Chrome:              >>> pytest --headless
# Headless Firefox:             >>> pytest --browser=firefox --headless

def pytest_addoption(parser):
    """Dodanie wlasnych opcji do uruchomienia skryptu testowania"""

    # Wlasna opcja wyboru przegladarki
    parser.addoption(
        "--browser", 
        action="store", 
        default="chrome", 
        help="Wybierz przegladarke: chrome lub firefox"
    )
    
    # Wlasna opcja wyboru trybu (graficzny czy headless)
    parser.addoption(
        "--headless",
        action="store_true",
        default=False,
        help="Uruchom testy w trybie headless (w tle, bez okna)"
    )


@pytest.fixture(scope="function")
def driver(request):

    # Pobieramy obie opcje z terminala
    browser_name = request.config.getoption("browser") 
    is_headless = request.config.getoption("headless") 
    
    driver = None

    # Sprawdzamy ktora przegladarka zostala wybrana
    if browser_name == "chrome":
        
        chrome_options = ChromeOptions()

        # Ignorujemy warning "Your connection is not private" ktore blokowalo prace skryptu
        chrome_options.accept_insecure_certs = True 
        chrome_options.add_argument("--ignore-certificate-errors")
        chrome_options.add_argument("--allow-insecure-localhost")
        chrome_options.add_argument("--ignore-ssl-errors")

        # Potrzebne dla WSL opcje
        chrome_options.add_argument("--no-sandbox") 
        chrome_options.add_argument("--disable-dev-shm-usage") 
        
        # Jesli wybrany tryb headless (bez okna), to do ustawien przegladarki dodac te opcje
        if is_headless: chrome_options.add_argument("--headless")
            
        driver = webdriver.Chrome(options=chrome_options) 

    elif browser_name == "firefox":
        
        firefox_options = FirefoxOptions()

        # Ignorujemy warning "Your connection is not private" ktore blokowalo prace skryptu
        firefox_options.accept_insecure_certs = True

        # Jesli wybrany tryb headless (bez okna), to do ustawien przegladarki dodac te opcje
        if is_headless: firefox_options.add_argument("--headless")

        driver = webdriver.Firefox(options=firefox_options) # Przekazujemy opcje
        
    else:
        raise pytest.UsageError(f"--browser={browser_name} jest nieobslugiwany")
    
    # Dodanie informacji w ktorym trybie dzialamy (zeby mozna bylo skorzystac w innych plikach)
    driver.is_headless = is_headless
    
    yield driver
    
    driver.quit()

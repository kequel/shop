import time
import os
import shutil

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from variables import COMPLETE_WINDOW_SLEEP_TIME, COMPLETE_SECTION_SLEEP_TIME


class OrderHistoryPage:

    # Lokator linku "Szczegoly"
    DETAILS_LINK = (By.CSS_SELECTOR, "a[data-link-action='view-order-details']")
    
    # Lokator sekcji ze szczegolami
    ORDER_INFOS = (By.ID, "order-infos")
    
    # Lokator ikonki PDF (faktura)
    INVOICE_BTN = (By.XPATH, "//a[contains(@href, 'controller=pdf-invoice')]")

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def go_to_details(self):
        """Wchodzi w szczegoly pierwszego zamowienia"""
        
        # Pobieramy liste przyciskow szczegolow i klikamy pierwszy
        details_btns = self.wait.until(EC.visibility_of_any_elements_located(self.DETAILS_LINK))
        
        if not details_btns: raise Exception("Brak zamowien w historii!")
            
        details_btns[0].click()
        
        # Czekamy az zaladuja sie szczegoly
        self.wait.until(EC.visibility_of_element_located(self.ORDER_INFOS))
        
        if not self.driver.is_headless: time.sleep(COMPLETE_WINDOW_SLEEP_TIME)

    def download_invoice(self):
        """Pobiera fakture klikajac w ikone PDF"""
        
        try:
            invoice_btn = self.wait.until(EC.element_to_be_clickable(self.INVOICE_BTN))
        except:
            raise Exception("Nie znaleziono przycisku faktury!")

        invoice_btn.click()
        time.sleep(5)

    def verify_invoice_downloaded(self):
        """Sprawdza folder downloads w poszukiwaniu nowego pliku PDF"""
        
        project_download_dir = os.path.abspath(os.path.join(os.getcwd(), "downloads"))
        
        system_download_dir = os.path.join(os.path.expanduser("~"), "Downloads")

        # Czekamy max 15 sekund na pojawienie sie pliku
        timeout = 15
        end_time = time.time() + timeout
        found_path = None
        found_file_name = None

        while time.time() < end_time:
            
            # Sprawdzamy folder projektu
            if os.path.exists(project_download_dir):
                for f in os.listdir(project_download_dir):
                    if f.endswith(".pdf"):
                        found_path = project_download_dir
                        found_file_name = f
                        break
            
            # Jesli nie znaleziono to sprawdzamy folder systemowy
            if not found_path and os.path.exists(system_download_dir):
                for f in os.listdir(system_download_dir):
                    if f.endswith(".pdf"):
                        file_full_path = os.path.join(system_download_dir, f)
                        if time.time() - os.path.getmtime(file_full_path) < 60:
                            found_path = system_download_dir
                            found_file_name = f
                            break
            
            if found_path:
                break
                
            time.sleep(1)

        if found_path:

            print(f"Znaleziono plik PDF: {found_file_name}")
            print(f"Lokalizacja: {found_path}")
            
        else:
            print(f"Zawartosc {project_download_dir}: {os.listdir(project_download_dir) if os.path.exists(project_download_dir) else 'Brak folderu'}")
            print(f"Zawartosc {system_download_dir}: {os.listdir(system_download_dir) if os.path.exists(system_download_dir) else 'Brak folderu'}")
            raise Exception("Nie znaleziono pliku PDF w zadnej lokalizacji.")
import time
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import json
import os

CATEGORY_SELECTOR = ".ets_mm_megamenu_content"
DEBUG_SAVE_HTML = False

# now saves results into ../scraping_results next to this script
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
OUTPUT_DIR = os.path.normpath(os.path.join(BASE_DIR, "..", "scraping_results"))
os.makedirs(OUTPUT_DIR, exist_ok=True)

def _outpath(filename: str) -> str:
    return os.path.join(OUTPUT_DIR, filename)

def extract_categories(html):
    soup = BeautifulSoup(html, "html.parser")
    menu = soup.select_one(CATEGORY_SELECTOR)
    if not menu:
        print("[ERROR] Nie znaleziono menu (", CATEGORY_SELECTOR, ")")
        return []

    categories = []

    for li in menu.select("li.mm_menus_li"):
        a = li.select_one("a[href]")
        if not a:
            continue
        name = a.get_text(strip=True)
        href = a["href"]

        subcats = []
        for sub_a in li.select(".ets_mm_categories a[href]"):
            subcats.append({
                "name": sub_a.get_text(strip=True),
                "url": sub_a["href"]
            })

        categories.append({
            "name": name,
            "url": href,
            "subcategories": subcats
        })

    return categories

def ProductsScraper(html):
    soup = BeautifulSoup(html, "html.parser")
    products = []

    for item in soup.select("#js-product-list li.product-miniature"):
        # link i nazwa
        a = item.select_one("a[href]")
        name = item.select_one(".product-name")
        url = item.select_one("a[href]")["href"] if a and a.has_attr("href") else None
        name = name["title"].strip() if name and name.has_attr("title") else (name.get_text(strip=True) if name else None)

        # cena netto i brutto
        price_netto = item.select_one(".price.discount, .price:not(.old-price)")
        price_netto = price_netto.get_text(strip=True).replace("\xa0", " ") if price_netto else None

        price_brutto = item.select_one(".old-price-tax")
        price_brutto = price_brutto.get_text(strip=True).replace("\xa0", " ") if price_brutto else None

        # producent
        manuf = item.select_one(".product-manufacturer-logo img")
        manufacturer = manuf["alt"].strip() if manuf and manuf.has_attr("alt") else None

        # symbol producenta
        symbol = item.select_one(".symbol_producenta")
        symbol = symbol.get_text(strip=True) if symbol else None

        # dostępność
        avail = item.select_one(".dostepnosc")
        availability = avail["title"].strip() if avail and avail.has_attr("title") else None

        # opis
        desc = item.select_one(".krotki_opis p")
        desc = desc.get_text(" ", strip=True) if desc else None


        if name and url:
            products.append({
                "name": name,
                "url": url,
                "symbol": symbol,
                "manufacturer": manufacturer,
                "price_netto": price_netto,
                "price_brutto": price_brutto,
                "availability": availability,
                "description": desc
            })

    return products


def main():
    with sync_playwright() as p:
        print("Otwieram przeglądarkę")
        browser = p.chromium.launch(
            headless=False,
            args=[
                "--ignore-certificate-errors",
                "--disable-blink-features=AutomationControlled"
            ]
        )
        context = browser.new_context(ignore_https_errors=True)
        page = context.new_page()
        page.route("**/*", lambda route, request: route.abort()
                        if request.resource_type == "image" else route.continue_())
        
        print("Wczytuję https://mopserwis.pl")
        page.goto("https://mopserwis.pl", wait_until="domcontentloaded", timeout=20000)

        try:
            page.locator("button:has-text('Zaakceptuj wszystkie')").first.click(timeout=500)
            time.sleep(0.2)
        except Exception:
            pass

        if "captcha" in page.url or "verify" in page.url:
            print("[UWAGA] Wykonaj ręcznie w przeglądarce weryfikację,")
            print("poczekaj aż strona się załaduje w pełni i naciśnij Enter...")
            input()

        html = page.content()

        if DEBUG_SAVE_HTML:
            with open(_outpath("mopserwis_full.html"), "w", encoding="utf-8") as f:
                f.write(html)

        cats = extract_categories(html)
        with open(_outpath("categories_mopserwis.json"), "w", encoding="utf-8") as f:
            json.dump(cats, f, ensure_ascii=False, indent=2)

        print(f"Zapisano {len(cats)} kategorii do categories_mopserwis.json")

        for cat in cats:

            print(f"Przetwarzam kategorię: {cat['name']} ({len(cat['subcategories'])} podkategorii)")
            #
            # TODO: Obecnie pobieramy linki do produktów tylko z podkategorii, imo nie ma sensu pobierać z 
            #       głównych kategorii bo to 2 razy więcej czasu a te same
            #       produkty są dostępne w podkategoriach.
            #
            # page.goto(cat["url"], wait_until="domcontentloaded", timeout=20000)
            

            # try:
            #     page.locator("button:has-text('Zaakceptuj wszystkie')").first.click(timeout=500)
            #     time.sleep(0.2)
            # except Exception:
            #     pass

            # for i in range(8):
            #     page.evaluate(f"window.scrollTo(0, {i}*document.body.scrollHeight/8)")
            #     try:
            #         page.wait_for_load_state("networkidle", timeout=3000)
            #     except:
            #         pass
            #     time.sleep(0.4)

            # if "captcha" in page.url or "verify" in page.url:
            #     print("[UWAGA] Wykonaj ręcznie w przeglądarce weryfikację,")
            #     print("poczekaj aż strona się załaduje w pełni i naciśnij Enter...")
            #     input()

            # cat_html = page.content()

            # if DEBUG_SAVE_HTML:
            #     filename = f"category_{cat['name'].replace(' ', '_')}.html"
            #     with open(_outpath(filename), "w", encoding="utf-8") as f:
            #         f.write(cat_html)

            # products = ProductsScraper(cat_html)
            # products_filename = f"products_{cat['name'].replace(' ', '_').replace('/', '#')}.json"
            # with open(_outpath(products_filename), "w", encoding="utf-8") as f:
            #     json.dump(products, f, ensure_ascii=False, indent=2)
            
            # print(f"Zapisano {len(products)} produktów z kategorii '{cat['name']}' do {products_filename}")

            for subcat in cat["subcategories"]:
                page.goto(subcat["url"], wait_until="domcontentloaded", timeout=20000)
                try:
                    page.locator("button:has-text('Zaakceptuj wszystkie')").first.click(timeout=500)
                    time.sleep(0.2)
                except Exception:
                    pass

                for i in range(8):
                    page.evaluate(f"window.scrollTo(0, {i}*document.body.scrollHeight/8)")
                    try:
                        page.wait_for_load_state("networkidle", timeout=2000)
                    except:
                        pass
                    time.sleep(0.4)

                if "captcha" in page.url or "verify" in page.url:
                    print("[UWAGA] Wykonaj ręcznie w przeglądarce weryfikację,")
                    print("poczekaj aż strona się załaduje w pełni i naciśnij Enter...")
                    input()

                subcat_html = page.content()

                if DEBUG_SAVE_HTML:
                    filename = f"subcategory_{subcat['name'].replace(' ', '_')}.html"
                    with open(_outpath(filename), "w", encoding="utf-8") as f:
                        f.write(subcat_html)

                products = ProductsScraper(subcat_html)
                products_filename = f"products_{subcat['name'].replace(' ', '_').replace('/', '#')}.json"
                with open(_outpath(products_filename), "w", encoding="utf-8") as f:
                    json.dump(products, f, ensure_ascii=False, indent=2)
                
                print(f"    Zapisano {len(products)} produktów z podkategorii '{subcat['name']}' do {products_filename}")

        browser.close()
        print(" --- Scraping zakończony. --- ")




if __name__ == "__main__":
    main()

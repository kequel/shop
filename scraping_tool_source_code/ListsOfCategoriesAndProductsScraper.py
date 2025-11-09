import time
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import json
import os
import re

CATEGORY_SELECTOR = ".ets_mm_megamenu_content"
DEBUG_SAVE_HTML = False
BASE_URL = "https://mopserwis.pl"

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
OUTPUT_DIR = os.path.normpath(os.path.join(BASE_DIR, "..", "scraping_results"))
os.makedirs(OUTPUT_DIR, exist_ok=True)

def _outpath(filename: str) -> str:
    return os.path.join(OUTPUT_DIR, filename)

def _safe_fname(s: str) -> str:
    s = s or "unnamed"
    return "".join(c if c.isalnum() or c in "._- " else "_" for c in s).replace(" ", "_")

def _accept_cookies(page):
    try:
        page.locator("button:has-text('Zaakceptuj wszystkie')").first.click(timeout=500)
        time.sleep(0.2)
    except Exception:
        pass

def _networkidle_soft(page, timeout=2000):
    try:
        page.wait_for_load_state("networkidle", timeout=timeout)
    except Exception:
        pass

def _ensure_not_captcha(page):
    if "captcha" in page.url or "verify" in page.url:
        print("[UWAGA] Zrób ręczną weryfikację w otwartej przeglądarce i ENTER…")
        input()

def _float_parse(s):
    if not s:
        return None
    s = s.replace("\xa0", " ").replace(",", ".").strip()
    m = re.search(r"[-+]?\d*\.?\d+", s)
    if m:
        try:
            return float(m.group(0) )
        except ValueError:
            return None
    return None

# ------------- PARSERY -----------------

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
        href = urljoin(BASE_URL, a["href"])

        subcats = []
        for sub_a in li.select(".ets_mm_categories a[href]"):
            subcats.append({
                "name": sub_a.get_text(strip=True),
                "url": urljoin(BASE_URL, sub_a["href"])
            })

        categories.append({
            "name": name,
            "url": href,
            "subcategories": subcats
        })

    return categories

# scraper danych ze strony listy produktów w kategorii - AKTUALNIE NIEPOTRZEBNY 
def ProductsScraper(html):
    
    products = []
    soup = BeautifulSoup(html, "html.parser")

    for item in soup.select("#js-product-list li.product-miniature"):
        a = item.select_one("a[href]")
        url = urljoin(BASE_URL, a["href"]) if a and a.has_attr("href") else None

        name = item.select_one(".product-name")
        name = name.get_text(strip=True) if name else None

        price_netto = item.select_one('[itemprop="price"]')
        price_netto = _float_parse(price_netto.get_text(strip=True).replace("\xa0", " ")) if price_netto else None

        price_brutto = item.select_one(".old-price-tax, .tax-inclusive")
        price_brutto = _float_parse(price_brutto.get_text(strip=True).replace("\xa0", " ")) if price_brutto else None

        manuf = item.select_one(".product-manufacturer-logo img, .brand img, .manufacturer img")
        manufacturer = manuf["alt"].strip() if manuf and manuf.has_attr("alt") else None


        avail = item.select_one(".dostepnosc, .availability, .product-availability")
        availability = avail.get("title", "").strip() if avail and avail.has_attr("title") else (avail.get_text(" ", strip=True) if avail else None)

        short_desc = item.select_one(".krotki_opis p, .product-description-short, .short_description")
        short_desc = short_desc.get_text(" ", strip=True) if short_desc else None

        if name and url:
            products.append({
                "name": name,
                "url": url,
                "manufacturer": manufacturer,
                "price_netto": price_netto,
                "price_brutto": price_brutto,
                "availability": availability,
                "description": short_desc
            })

    return products

def DetailProductScraper(html, current_url=None, prod_from_list=None):
    soup = BeautifulSoup(html, "html.parser")

    # nazwa
    nm = soup.select_one("h2.product-name")
    detail_name = nm.get_text(strip=True) if nm else (prod_from_list or {}).get("name")

    # product id
    product_id = soup.select_one('input[name="id_product"][type="hidden"]')


    # opis długi
    long_desc = soup.select_one('.product-description')
    # opis krótki 
    short_desc_el = soup.select_one('meta[property="og:description"]')
    short_desc = short_desc_el["content"].strip() if short_desc_el and short_desc_el.has_attr("content") else None



    # obrazy
    images = []
    for img in soup.select("#product-slider-navigation-list img, .product-slider-navigation-wrap img"):
        u = img.get("src")
        if not u:
            continue
        u = urljoin(BASE_URL, u)
        images.append(u)
    images = list(set(images))  # Usuń duplikaty
    images = [x.replace("home_default", "large_default") for x in images]


    # dostępność
    avail_el = soup.select_one('#product-availability')
    availability = None
    if avail_el:
        icon = avail_el.select_one('i[title]')
        if icon and icon.has_attr('title'):
            availability = icon['title'].strip()
        else:
            availability = avail_el.get_text(" ", strip=True)

    # producent
    manuf_el = soup.select_one('.manufacturer, .product-manufacturer, .product-brand, .producer, .product-manufacturer a')
    manufacturer = manuf_el.get_text(" ", strip=True) if manuf_el else ((prod_from_list or {}).get("manufacturer"))

    # waga produktu (meta property/name "product:weight:value")
    weight_tag = soup.select_one('meta[property="product:weight:value"]')
    weight = None
    if weight_tag and weight_tag.has_attr("content"):
        weight = _float_parse(weight_tag["content"].strip())

    weight_unit_tag = soup.select_one('meta[property="product:weight:units"]')
    weight_unit = weight_unit_tag["content"].strip() if weight_unit_tag and weight_unit_tag.has_attr("content") else None

    price_brutto_tag = soup.select_one('meta[property="product:price:amount"]')
    price_brutto = _float_parse(price_brutto_tag["content"].strip()) if price_brutto_tag and price_brutto_tag.has_attr("content") else None

    price_netto_tag = soup.select_one('meta[property="product:pretax_price:amount"]')
    price_netto = _float_parse(price_netto_tag["content"].strip()) if price_netto_tag and price_netto_tag.has_attr("content") else None

    currency_tag = soup.select_one('meta[property="product:price:currency"]')
    currency = currency_tag["content"].strip() if currency_tag and currency_tag.has_attr("content") else None



    detail = {
        "product_id": product_id["value"] if product_id and product_id.has_attr("value") else None,
        "name": detail_name,
        "url": current_url,
        "long_description": str(long_desc) if long_desc else None,
        "images": images,
        "availability": availability,
        "manufacturer": manufacturer,
        "weight": weight,
        "weight_unit": weight_unit,
        "price_netto": price_netto,
        "price_brutto": price_brutto,
        "currency": currency,
        "short_description": short_desc
    }

    # scalenie z listy - TYMCZASOWO WYŁĄCZONE
    if prod_from_list and False :
        detail.update({
            
        })

    return detail

# ----------- FLOW STRONY / SCRAP --------------

def paginate_and_collect_products(page):
    """Zbiera produkty z bieżącej podkategorii po wszystkich stronach paginacji."""
    all_products = []
    visited_urls = set()

    while True:
        _ensure_not_captcha(page)
        _accept_cookies(page)
        _networkidle_soft(page)

        # przewiń kilka razy żeby dociągnąć lazy DOM
        for i in range(6):
            page.evaluate(f"window.scrollTo(0, {i+1}*document.body.scrollHeight/6)")
            _networkidle_soft(page, timeout=1500)
            time.sleep(0.2)

        html = page.content()
        if DEBUG_SAVE_HTML:
            with open(_outpath(f"page_{int(time.time())}.html"), "w", encoding="utf-8") as f:
                f.write(html)

        products = ProductsScraper(html)
        all_products.extend(products)

        # spróbuj kliknąć "następna strona"
        soup = BeautifulSoup(html, "html.parser")
        next_link = soup.select_one('a[rel="next"], .pagination a.next, .page-list a.next')
        if not next_link:
            # spróbuj po tekście
            for a in soup.select(".pagination a, .page-list a"):
                if "następ" in a.get_text(strip=True).lower() or "next" in a.get_text(strip=True).lower():
                    next_link = a
                    break

        if next_link:
            next_url = urljoin(page.url, next_link.get("href"))
            if next_url in visited_urls:
                break
            visited_urls.add(next_url)
            page.goto(next_url, wait_until="domcontentloaded", timeout=20000)
            continue
        break

    # deduplikacja po URL
    dedup = {p["url"]: p for p in all_products if p.get("url")}
    return list(dedup.values())

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

        # blokuj obrazy (oszczędność transferu/anty-bot-friendly)
        page.route("**/*", lambda route, request: route.abort()
                   if request.resource_type == "image" else route.continue_())

        print(f"Wczytuję {BASE_URL}")
        page.goto(BASE_URL, wait_until="domcontentloaded", timeout=20000)
        _accept_cookies(page)
        _ensure_not_captcha(page)
        _networkidle_soft(page)

        html = page.content()
        if DEBUG_SAVE_HTML:
            with open(_outpath("mopserwis_full.html"), "w", encoding="utf-8") as f:
                f.write(html)

        cats = extract_categories(html)
        with open(_outpath("categories_mopserwis.json"), "w", encoding="utf-8") as f:
            json.dump(cats, f, ensure_ascii=False, indent=2)
        print(f"Zapisano {len(cats)} kategorii do categories_mopserwis.json")

        # ----------- iteracja po kategoriach/podkategoriach -------------
        for cat in cats:
            print(f"[KATEGORIA] {cat['name']} ({len(cat['subcategories'])} podkategorii)")

            for subcat in cat["subcategories"]:
                print(f"  [PODKAT] {subcat['name']}")
                page.goto(subcat["url"], wait_until="domcontentloaded", timeout=20000)
                _accept_cookies(page)
                _ensure_not_captcha(page)

                # zbierz produkty w całej paginacji
                products = paginate_and_collect_products(page)
                print(f"    >> Zebrano {len(products)} produktów z '{subcat['name']}'")

                # szczegóły produktów
                product_details = []
                for idx, prod in enumerate(products, 1):
                    print(f"        [{idx}/{len(products)}] {prod.get('name')}")
                    page.goto(prod["url"], wait_until="domcontentloaded", timeout=20000)
                    _accept_cookies(page)
                    _ensure_not_captcha(page)

                    # lekki scroll aby dociągnąć content
                    for i in range(4):
                        page.evaluate(f"window.scrollTo(0, {i+1}*document.body.scrollHeight/4)")
                        _networkidle_soft(page, timeout=1500)
                        time.sleep(0.2)

                    prod_html = page.content()
                    detail = DetailProductScraper(prod_html, current_url=page.url, prod_from_list=prod)
                    product_details.append(detail)
                    time.sleep(0.1)

                # zapis
                details_fname = f"products_details_{_safe_fname(subcat.get('name') or 'subcategory')}.json"
                with open(_outpath(details_fname), "w", encoding="utf-8") as f:
                    json.dump(product_details, f, ensure_ascii=False, indent=2)
                print(f"    Zapisano szczegóły {len(product_details)} produktów -> {details_fname}")

        browser.close()
        print(" --- Scraping zakończony. --- ")

if __name__ == "__main__":
    main()

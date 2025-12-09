import time
import json
import os
import re
import random
import urllib.request
from urllib.parse import urljoin, urlparse

from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup

CATEGORY_SELECTOR = ".ets_mm_megamenu_content"
DEBUG_SAVE_HTML = False
BASE_URL = "https://mopserwis.pl"

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
OUTPUT_DIR = os.path.normpath(os.path.join(BASE_DIR, "..", "scraping_results"))
os.makedirs(OUTPUT_DIR, exist_ok=True)

IMAGES_DIR = os.path.join(OUTPUT_DIR, "product_images")
os.makedirs(IMAGES_DIR, exist_ok=True)


def _outpath(filename: str) -> str:
    """Zwraca pełną ścieżkę pliku w katalogu OUTPUT_DIR."""
    return os.path.join(OUTPUT_DIR, filename)


def _safe_fname(s: str) -> str:
    """Zamienia tekst na bezpieczną nazwę pliku (bez dziwnych znaków, spacje -> podkreślenia)."""
    s = s or "unnamed"
    return "".join(c if c.isalnum() or c in "._- " else "_" for c in s).replace(" ", "_")


def _accept_cookies(page):
    """Próbuje kliknąć przycisk akceptacji cookies, jeśli jest widoczny."""
    try:
        page.locator("button:has-text('Zaakceptuj wszystkie')").first.click(timeout=500)
        time.sleep(0.2)
    except Exception:
        pass


def _networkidle_soft(page, timeout=2000):
    """Miękkie czekanie na 'networkidle' (ignoruje wyjątki przy wolnych stronach)."""
    try:
        page.wait_for_load_state("networkidle", timeout=timeout)
    except Exception:
        pass


def _ensure_not_captcha(page):
    """Zatrzymuje wykonywanie, jeśli Playwright trafi na stronę z CAPTCHA/verify."""
    if "captcha" in page.url or "verify" in page.url:
        print("[UWAGA] Zrób ręczną weryfikację w otwartej przeglądarce i ENTER…")
        input()


def _float_parse(s):
    """Wyciąga pierwszą liczbę zmiennoprzecinkową z napisu (np. '1 234,50 zł' -> 1234.5)."""
    if not s:
        return None
    s = s.replace("\xa0", " ").replace(",", ".").strip()
    m = re.search(r"[-+]?\d*\.?\d+", s)
    if m:
        try:
            return float(m.group(0))
        except ValueError:
            return None
    return None


def _download_product_images(image_urls, category, subcategory, product_name, limit=2):
    """
    Pobiera do `limit` obrazów produktu i zwraca ścieżki względne względem OUTPUT_DIR.
    Zapisuje obrazy w strukturze: IMAGES_DIR/kategoria/podkategoria/nazwa_produktu_1.jpg
    """
    if not image_urls:
        return []

    cat_dir = _safe_fname(category or "uncategorized")
    sub_dir = _safe_fname(subcategory or "no_subcategory")
    base_folder = os.path.join(IMAGES_DIR, cat_dir, sub_dir)
    os.makedirs(base_folder, exist_ok=True)

    downloaded = []
    for i, img_url in enumerate(image_urls[:limit]):
        try:
            parsed = urlparse(img_url)
            _, ext = os.path.splitext(parsed.path)
            if not ext or len(ext) > 5:
                ext = ".jpg"

            fname = f"{_safe_fname(product_name or 'product')}_{i+1}{ext}"
            filepath = os.path.join(base_folder, fname)

            urllib.request.urlretrieve(img_url, filepath)
            rel_path = os.path.relpath(filepath, OUTPUT_DIR)
            downloaded.append(rel_path)
        except Exception as e:
            print(f"[WARN] Nie udało się pobrać obrazu {img_url}: {e}")
            continue

    return downloaded


def extract_categories(html):
    """Parsuje stronę główną i wyciąga listę kategorii z podkategoriami."""
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


def ProductsScraper(html):
    """Parsuje stronę listy produktów i zwraca listę podstawowych informacji o produktach."""
    products = []
    soup = BeautifulSoup(html, "html.parser")

    for item in soup.select("#js-product-list li.product-miniature"):
        a = item.select_one("a[href]")
        url = urljoin(BASE_URL, a["href"]) if a and a.has_attr("href") else None

        name = item.select_one(".product-name")
        name = name.get_text(strip=True) if name else None

        price_netto_el = item.select_one('[itemprop="price"]')
        price_netto = _float_parse(price_netto_el.get_text(strip=True).replace("\xa0", " ")) if price_netto_el else None

        price_brutto_el = item.select_one(".old-price-tax, .tax-inclusive")
        price_brutto = _float_parse(price_brutto_el.get_text(strip=True).replace("\xa0", " ")) if price_brutto_el else None

        manuf = item.select_one(".product-manufacturer-logo img, .brand img, .manufacturer img")
        manufacturer = manuf["alt"].strip() if manuf and manuf.has_attr("alt") else None

        avail = item.select_one(".dostepnosc, .availability, .product-availability")
        availability = (
            avail.get("title", "").strip()
            if avail and avail.has_attr("title")
            else (avail.get_text(" ", strip=True) if avail else None)
        )

        short_desc_el = item.select_one(".krotki_opis p, .product-description-short, .short_description")
        short_desc = short_desc_el.get_text(" ", strip=True) if short_desc_el else None

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


def DetailProductScraper(html, current_url=None, prod_from_list=None, category=None, subcategory=None):
    """
    Parsuje stronę szczegółu produktu i zwraca pełen zestaw danych:

    """
    soup = BeautifulSoup(html, "html.parser")

    nm = soup.select_one("h2.product-name")
    detail_name = nm.get_text(strip=True) if nm else (prod_from_list or {}).get("name")

    product_id = soup.select_one('input[name="id_product"][type="hidden"]')
    long_desc = soup.select_one('.product-description')

    short_desc_el = soup.select_one('meta[property="og:description"]')
    short_desc = short_desc_el["content"].strip() if short_desc_el and short_desc_el.has_attr("content") else None

    images = []
    for img in soup.select("#product-slider-navigation-list img, .product-slider-navigation-wrap img"):
        u = img.get("src")
        if not u:
            continue
        u = urljoin(BASE_URL, u)
        images.append(u)
    images = list(set(images))
    images = [x.replace("home_default", "large_default") for x in images]

    avail_el = soup.select_one('#product-availability')
    availability = None
    if avail_el:
        icon = avail_el.select_one('i[title]')
        if icon and icon.has_attr('title'):
            availability = icon['title'].strip()
        else:
            availability = avail_el.get_text(" ", strip=True)

    weight = None
    weight_tag = soup.select_one('meta[property="product:weight:value"]')
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

    quantity = None
    if availability == "Produkt dostępny":
        quantity = random.randint(2, 50)

    manuf_el = soup.select_one('.manufacturer, .product-manufacturer, .product-brand, .producer, .product-manufacturer a')
    if manuf_el:
        manufacturer = manuf_el.get_text(" ", strip=True)
    else:
        manufacturer = (prod_from_list or {}).get("manufacturer")

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
        "short_description": short_desc,
        "category_name": subcategory,
        "main_category_name": category,
        "quantity": quantity,
    }

    return detail


def paginate_and_collect_products(page):
    """
    Zbiera produkty z aktualnej podkategorii, przechodząc przez całą paginację.

    - Scrollowanie strony w kilku krokach, żeby dociągnąć lazy-loadowane elementy.
    - Wyszukiwanie linka "następna strona" po selektorze i po tekście.
    """
    all_products = []
    visited_urls = set()

    while True:
        _ensure_not_captcha(page)
        _accept_cookies(page)
        _networkidle_soft(page)

        for i in range(6):
            page.evaluate(f"window.scrollTo(0, {(i + 1)}*document.body.scrollHeight/6)")
            _networkidle_soft(page, timeout=1500)
            time.sleep(0.2)

        html = page.content()
        if DEBUG_SAVE_HTML:
            with open(_outpath(f"page_{int(time.time())}.html"), "w", encoding="utf-8") as f:
                f.write(html)

        products = ProductsScraper(html)
        all_products.extend(products)

        soup = BeautifulSoup(html, "html.parser")
        next_link = soup.select_one('a[rel="next"], .pagination a.next, .page-list a.next')
        if not next_link:
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

    # deduplikacja po URL – ten sam produkt może pokazać się kilka razy, np. przy błędnej paginacji
    dedup = {p["url"]: p for p in all_products if p.get("url")}
    return list(dedup.values())


def main():
    """Główna procedura: uruchamia przeglądarkę, zbiera kategorie, produkty i zapisuje JSON + obrazy."""
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

        # blokowanie obrazów w Playwright (HTML i tak zawiera src, więc można pobierać je ręcznie)
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

        for cat in cats:
            print(f"[KATEGORIA] {cat['name']} ({len(cat['subcategories'])} podkategorii)")

            for subcat in cat["subcategories"]:
                print(f"  [PODKAT] {subcat['name']}")
                page.goto(subcat["url"], wait_until="domcontentloaded", timeout=20000)
                _accept_cookies(page)
                _ensure_not_captcha(page)

                products = paginate_and_collect_products(page)
                print(f"    >> Zebrano {len(products)} produktów z '{subcat['name']}'")

                product_details = []
                for idx, prod in enumerate(products, 1):
                    print(f"        [{idx}/{len(products)}] {prod.get('name')}")
                    page.goto(prod["url"], wait_until="domcontentloaded", timeout=20000)
                    _accept_cookies(page)
                    _ensure_not_captcha(page)

                    for i in range(4):
                        page.evaluate(f"window.scrollTo(0, {(i + 1)}*document.body.scrollHeight/4)")
                        _networkidle_soft(page, timeout=1500)
                        time.sleep(0.2)

                    prod_html = page.content()
                    detail = DetailProductScraper(
                        prod_html,
                        current_url=page.url,
                        prod_from_list=prod,
                        category=cat["name"],
                        subcategory=subcat["name"],
                    )

                    downloaded_files = _download_product_images(
                        detail.get("images", []),
                        category=cat["name"],
                        subcategory=subcat["name"],
                        product_name=detail.get("name"),
                    )
                    detail["downloaded_images"] = downloaded_files

                    product_details.append(detail)
                    time.sleep(0.1)

                details_fname = f"products_details_{_safe_fname(subcat.get('name') or 'subcategory')}.json"
                with open(_outpath(details_fname), "w", encoding="utf-8") as f:
                    json.dump(product_details, f, ensure_ascii=False, indent=2)
                print(f"    Zapisano szczegóły {len(product_details)} produktów -> {details_fname}")

        browser.close()
        print(" --- Scraping zakończony. --- ")


if __name__ == "__main__":
    main()

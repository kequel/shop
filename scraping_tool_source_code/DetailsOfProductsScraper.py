import os
import re
import json
import time
from urllib.parse import urljoin

from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup

# ========== USTAWIENIA ==========

CATEGORY_SELECTOR = ".ets_mm_megamenu_content"  # (niewykorzystywane tutaj, zostawione dla zgodności)
DEBUG_SAVE_HTML = False

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
OUTPUT_DIR = os.path.normpath(os.path.join(BASE_DIR, "..", "scraping_results"))
os.makedirs(OUTPUT_DIR, exist_ok=True)

def _outpath(filename: str) -> str:
    return os.path.join(OUTPUT_DIR, filename)

# ========== POMOCNICZE ==========

def _txt(el):
    return el.get_text(" ", strip=True) if el else None

def _attr(node, *names):
    if not node: return None
    for n in names:
        if node.has_attr(n): return node[n]
    return None

def _num(x):
    """parsuje tekst typu '154,90 zł' -> 154.90 (float)"""
    if x is None: return None
    # usuń nbsp/ spacje, zł itp.
    s = str(x).replace("\xa0", " ").replace(" ", "")
    s = s.replace("zł","").replace("PLN","")
    # zamień przecinek na kropkę i wytnij wszystko poza 0-9 i kropką
    s = s.replace(",", ".")
    m = re.findall(r"\d+(?:\.\d+)?", s)
    return float(m[0]) if m else None

def _meta(soup, prop):
    tag = soup.select_one(f'meta[property="{prop}"]')
    return tag.get("content") if tag and tag.has_attr("content") else None

def _images(soup, base_url=None):
    out = []
    for img in soup.select("#product-slider-navigation-list img, .product-slider-navigation-wrap img"):
        u = img.get("src")
        if not u:
            continue
        if base_url:
            u = urljoin(base_url, u)
        out.append(u)
    out = list(set(out))  # Usuń duplikaty
    out = [x.replace("home_default", "large_default") for x in out]
    return out

def _product_id(soup):
    body = soup.select_one("body")
    if not body: return None
    for c in body.get("class", []):
        m = re.match(r"product-id-(\d+)", c)
        if m: return m.group(1)
    return None

def _ean_from_url(url):
    if not url: return None
    m = re.search(r"(\d{8,14})(?:\.html)?$", url)
    return m.group(1) if m else None

def _regular_price_text(soup):
    # najczęściej:
    cand = (soup.select_one(".price-striked") or
            soup.select_one(".regular-price") or
            soup.select_one(".old-price") or
            soup.select_one(".product-unit-price-before-discount"))
    return _txt(cand)

def _netto_text(soup):
    b = soup.select_one(".netto")
    if not b: return None
    for sp in b.select("span"):
        t = sp.get_text(strip=True)
        if any(ch.isdigit() for ch in t):
            return t
    return None

def DetailProductScraper(html, base_url=None, current_url=None):
    soup = BeautifulSoup(html, "html.parser")


    name = _txt(soup.select_one(".product-name"))
    product_id = _product_id(soup)
    ean = _ean_from_url(current_url)

    price_gross = _num(_meta(soup, "product:price:amount"))
    currency = _meta(soup, "product:price:currency") or "PLN"

    price_net = _num(_meta(soup, "product:pretax_price:amount"))
    if price_net is None:
        price_net = _num(_netto_text(soup))

    price_regular_gross = _num(_regular_price_text(soup))
    if price_regular_gross is None:
        pr_node = soup.select_one('.current-price [itemprop="price"]') or soup.select_one('span[itemprop="price"]')
        price_gross = price_gross or _num(_txt(pr_node))

    on_promo = bool(price_regular_gross and price_gross and price_regular_gross > price_gross)
    discount_percent = round((price_regular_gross - price_gross) / price_regular_gross * 100, 2) if on_promo else None

    vat_rate_percent = None
    if price_gross and price_net and price_net > 0:
        vat_rate_percent = round((price_gross / price_net - 1) * 100, 2)

    manuf_img = soup.select_one(".product-manufacturer img, .manufacturer-logo img")
    manuf_link = soup.select_one(".product-manufacturer a, .manufacturer-name a")
    manufacturer = (manuf_img.get("alt").strip() if manuf_img and manuf_img.has_attr("alt") else None) or _txt(manuf_link)

    symbol = (_txt(soup.select_one(".product-reference .editable")) or
              _txt(soup.select_one("#product-details .product-reference")) or
              _txt(soup.select_one(".product-reference span")))

    availability_text = _txt(soup.select_one(".product-quantities span, #product-availability, .availability span"))
    description = _txt(soup.select_one("#tab-content-description")) or _txt(soup.select_one("#description, .product-description"))
    images = _images(soup, base_url=base_url)

    return [{
        "url": current_url,
        "product_id": product_id,
        "ean": ean,
        "name": name,
        "manufacturer": manufacturer,
        "symbol": symbol,
        "availability_text": availability_text,
        "description": description,
        "images": images,

        "currency": currency,
        "price_gross": price_gross,
        "price_net": price_net,
        "price_regular_gross": price_regular_gross,
        "on_promo": on_promo,
        "discount_percent": discount_percent,
        "vat_rate_percent": vat_rate_percent
    }]

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

        page.route(
            "**/*",
            lambda route, request: route.abort()
            if request.resource_type in {"image", "media", "font"}
            else route.continue_()
        )

        files_to_process = [
            "products_Tork_Linia_Biała.json",
            # dodaj kolejne pliki tutaj
        ]

        for file_name in files_to_process:
            file_path = file_name if os.path.isabs(file_name) else _outpath(file_name)

            if not os.path.exists(file_path):
                print(f"Plik nie istnieje: {file_path} — pomijam.")
                continue

            urls = []
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    data = json.load(f)

                if isinstance(data, list):
                    for item in data:
                        if isinstance(item, str):
                            urls.append(item)
                        elif isinstance(item, dict):
                            u = item.get("url")
                            if u:
                                urls.append(u)
                elif isinstance(data, dict):
                    for k in ("url", "link", "href"):
                        if k in data and isinstance(data[k], str):
                            urls.append(data[k])
            except Exception as e:
                print("Nie można wczytać pliku:", file_path, e)
                continue

            if not urls:
                print(f"Brak URLi w {file_path} — pomijam.")
                continue

            print(f"Wczytano {len(urls)} URLi z {file_path}")

            all_products = []
            for idx, url in enumerate(urls, start=1):
                try:
                    print(f"[{idx}/{len(urls)}] Otwieram {url}")
                    page.goto(url, wait_until="domcontentloaded", timeout=20000)
                    time.sleep(0.5)

                    try:
                        page.locator("button:has-text('Zaakceptuj wszystkie')").first.click(timeout=500)
                        time.sleep(0.2)
                    except Exception:
                        pass

                    try:
                        page.wait_for_selector("h1.h1", timeout=5000)
                    except Exception:
                        pass

                    if "captcha" in page.url or "verify" in page.url:
                        print("[UWAGA] Wykonaj ręcznie w przeglądarce weryfikację,")
                        print("poczekaj aż strona się załaduje w pełni i naciśnij Enter...")
                        input()

                    html = page.content()

                    if DEBUG_SAVE_HTML:
                        safe = url.replace("://", "_").replace("/", "_").replace("?", "_").replace("&", "_").replace("=", "_")
                        with open(_outpath(f"raw_{safe[:120]}.html"), "w", encoding="utf-8") as f:
                            f.write(html)

                    products = DetailProductScraper(
                        html,
                        base_url="https://mopserwis.pl",
                        current_url=page.url
                    )
                    all_products.extend(products)

                    # # opcjonalnie: zapis per-URL
                    # per_url_filename = f"details_{idx:04d}.json"
                    # with open(_outpath(per_url_filename), "w", encoding="utf-8") as f:
                    #     json.dump(products, f, ensure_ascii=False, indent=2)

                except Exception as e:
                    print(f"Błąd podczas przetwarzania {url}:", e)

            out_filename = f"details_{os.path.basename(file_path)}"
            with open(_outpath(out_filename), "w", encoding="utf-8") as f:
                json.dump(all_products, f, ensure_ascii=False, indent=2)
            print(f"Zapisano łącznie {len(all_products)} produktów do {out_filename}")

        browser.close()
        print(" --- Scraping zakończony. --- ")

if __name__ == "__main__":
    main()

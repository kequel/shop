

document.addEventListener('click', (e) => {
  const banner = e.target.closest('.banner, .carousel, .homeslider');
  if (!banner) return;

  if (typeof gtag === 'function') {
    gtag('event', 'banner_use', {
      banner_name: (banner.textContent || '').trim().slice(0, 60)
    });
  }
});


document.addEventListener('click', (e) => {
  const btn = e.target.closest('button.add-to-cart, #dodaj1, [data-button-action="add-to-cart"]');
  if (!btn) return;

  const card = btn.closest('.thumbnail-container');
  if (!card) return;

  const promoFlag = card.querySelector('li.product-flag.discount, .discount-percentage');
  if (!promoFlag) return;

  const form = btn.closest('form');
  const idProduct = form?.querySelector('input[name="id_product"]')?.value || '';

  if (typeof gtag === 'function') {
    gtag('event', 'promo_add_to_cart', {
      id_product: idProduct,
      promo_label: (promoFlag.textContent || '').trim().slice(0, 30),
      source: 'product_list'
    });
  }
}, true);


(function () {

  function parsePrice(text) {
    return Number(
      (text || "")
        .replace(/\u00A0/g, " ")
        .replace(/[^0-9,.\-]/g, "")
        .replace(",", ".")
    ) || 0;
  }

  document.addEventListener("DOMContentLoaded", function () {
    if (!document.body || document.body.id !== "order-confirmation") return;
    if (typeof gtag !== "function") return;

    const url = new URL(window.location.href);
    const idOrder = (url.searchParams.get("id_order") || "").trim();

    const refEl = document.querySelector("#order-reference-value");
    const refText = refEl ? (refEl.textContent || "").trim() : "";
    const refMatch = refText.match(/Numer zamówienia:\s*([A-Z0-9-]+)/i);
    const orderRef = refMatch ? refMatch[1] : "";

    const transactionId = idOrder || orderRef || ("order_" + Date.now());

    let value = 0;
    const payReturnDl = document.querySelector("#content-hook_payment_return dl");
    if (payReturnDl) {
      const dds = payReturnDl.querySelectorAll("dd");
      if (dds && dds.length > 0) {
        value = parsePrice(dds[0].textContent);
      }
    }

    const currency =
      (window.prestashop && prestashop.currency && prestashop.currency.iso_code) ||
      "PLN";

    const dedupeKey = "ga_purchase_sent_" + transactionId;
    if (sessionStorage.getItem(dedupeKey) === "1") return;
    sessionStorage.setItem(dedupeKey, "1");

    gtag("event", "purchase", {
      transaction_id: transactionId,
      value: value,
      currency: currency
    });
    //debug
    console.log("[GA] purchase sent", {
      transaction_id: transactionId,
      value: value,
      currency: currency
    });
  });

})();

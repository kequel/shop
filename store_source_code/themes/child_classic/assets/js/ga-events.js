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

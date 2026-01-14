document.addEventListener('click', (e) => {
  const banner = e.target.closest('.banner, .carousel, .homeslider');
  if (!banner) return;

  if (typeof gtag === 'function') {
    gtag('event', 'banner_use', {
      banner_name: (banner.textContent || '').trim().slice(0, 60)
    });
  }
});

if (window.prestashop) {
  prestashop.on('updateCart', () => {
    const promo = document.querySelector('.product-flag.discount, .product-flag.on-sale, .on-sale');
    if (!promo) return;

    if (typeof gtag === 'function') {
      gtag('event', 'promo_add_to_cart', { source: 'cart' });
    }
  });
}

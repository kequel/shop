{**
 * Copyright since 2007 PrestaShop SA and Contributors
 * PrestaShop is an International Registered Trademark & Property of PrestaShop SA
 *
 * NOTICE OF LICENSE
 *
 * This source file is subject to the Academic Free License 3.0 (AFL-3.0)
 * that is bundled with this package in the file LICENSE.md.
 * It is also available through the world-wide-web at this URL:
 * https://opensource.org/licenses/AFL-3.0
 * If you did not receive a copy of the license and are unable to
 * obtain it through the world-wide-web, please send an email
 * to license@prestashop.com so we can send you a copy immediately.
 *
 * DISCLAIMER
 *
 * Do not edit or add to this file if you wish to upgrade PrestaShop to newer
 * versions in the future. If you wish to customize PrestaShop for your
 * needs please refer to https://devdocs.prestashop.com/ for more information.
 *
 * @author    PrestaShop SA and Contributors <contact@prestashop.com>
 * @copyright Since 2007 PrestaShop SA and Contributors
 * @license   https://opensource.org/licenses/AFL-3.0 Academic Free License 3.0 (AFL-3.0)
 *}
{block name='product_miniature_item'}
<div class="js-product product{if !empty($productClasses)} {$productClasses}{/if}">
  <article class="product-miniature js-product-miniature" data-id-product="{$product.id_product}" data-id-product-attribute="{$product.id_product_attribute}">
    <div class="thumbnail-container">
      <div class="thumbnail-top">
        {block name='product_thumbnail'}
          {if $product.cover}
            <a href="{$product.url}" class="thumbnail product-thumbnail">
              <img
                src="{$product.cover.bySize.home_default.url}"
                alt="{if !empty($product.cover.legend)}{$product.cover.legend}{else}{$product.name}{/if}"
                loading="lazy"
                data-full-size-image-url="{$product.cover.large.url}"
                width="{$product.cover.bySize.home_default.width}"
                height="{$product.cover.bySize.home_default.height}"
              />
            </a>
          {else}
            <a href="{$product.url}" class="thumbnail product-thumbnail">
              <img
                src="{$urls.no_picture_image.bySize.home_default.url}"
                loading="lazy"
                width="{$urls.no_picture_image.bySize.home_default.width}"
                height="{$urls.no_picture_image.bySize.home_default.height}"
              />
            </a>
          {/if}
        {/block}

        
      </div>

      <div class="product-description1">
        {block name='product_name'}
          {if $page.page_name == 'index'}
            <h3 class="h3 product-title"><a href="{$product.url}" content="{$product.url}">{$product.name}</a></h3>
          {else}
            <h2 class="h3 product-title"><a href="{$product.url}" content="{$product.url}">{$product.name}</a></h2>
          {/if}
        {/block}

        {block name='product_price_and_shipping'}
          {if $product.show_price}

            <div class="product-price-and-shipping">

              {if $product.has_discount}
                {hook h='displayProductPriceBlock' product=$product type="old_price"}

                
                {if $product.discount_type === 'percentage'}
                  <span class="discount-percentage discount-product">{$product.discount_percentage}</span>
                {elseif $product.discount_type === 'amount'}
                  <span class="discount-amount discount-product">{$product.discount_amount_to_display}</span>
                {/if}
              {/if}
      

              {hook h='displayProductPriceBlock' product=$product type="before_price"}


              <div class="dostepnosc dostepny"></div>
              <span class="price" aria-label="{l s='Price' d='Shop.Theme.Catalog'}">
                {capture name='custom_price'}{hook h='displayProductPriceBlock' product=$product type='custom_price' hook_origin='products_list'}{/capture}
                {if '' !== $smarty.capture.custom_price}
                  {$smarty.capture.custom_price nofilter}
                {else}
                  {$product.price_tax_exc|number_format:2:'.':' '} zł
                {/if}
              </span>
              <div id="z_vatem">
                {$product.price} z VAT
                
              </div>

              {hook h='displayProductPriceBlock' product=$product type='unit_price'}

              {hook h='displayProductPriceBlock' product=$product type='weight'}
              
            </div>
          {/if}
          
          
          <div id="dodaj_do_koszyka">
              <form action="http://localhost:8080/cart" method="post" id="add-to-cart-or-refresh">
              <input type="hidden" name="token" value="ec77e8c82bb21ce2ddf48940f7ecbd54">
              <input type="hidden" name="id_product" value="2255">
		
		          <div id="plusminus" style="display:inline-block; float:left;"> 
                <button style=" display:inline-block; padding: 2.5px 5px;" type="button" id="sub" class="sub">-</button>
                <input style=" display:inline-block; width:30px;    display: inline-block;width: 30px; height: 26px; padding: 2px 0px; text-align: center;" type="" name="qty" value="1" min="1" data-button-action="add-to-cart">
                <button style="display:inline-block; padding: 2.5px 5px;" type="button" id="add" class="add">+</button>
              </div>
<script>
document.addEventListener('DOMContentLoaded', function() {
  document.querySelectorAll('#plusminus').forEach(function(container) {
    const addBtn = container.querySelector('.add');
    const subBtn = container.querySelector('.sub');
    const qtyInput = container.querySelector('input[name="qty"]');

    addBtn.replaceWith(addBtn.cloneNode(true));
    subBtn.replaceWith(subBtn.cloneNode(true));

    const newAddBtn = container.querySelector('.add');
    const newSubBtn = container.querySelector('.sub');

    newAddBtn.addEventListener('click', function(e) {
      e.preventDefault();
      let value = parseInt(qtyInput.value) || 1;
      qtyInput.value = value + 1;
    });

    newSubBtn.addEventListener('click', function(e) {
      e.preventDefault();
      let value = parseInt(qtyInput.value) || 1;
      const min = parseInt(qtyInput.min) || 1;
      if (value > min) {
        qtyInput.value = value - 1;
      }
    });
  });
});
</script>


	
		
        <a id="dodaj1" class="button add-to-cart" href="#" data-button-action="add-to-cart" data-url="https://mopserwis.pl/koszyk?add=1&amp;id_product=2255&amp;id_product_attribute=0"><i class="fa fa-cart-plus"></i> Do koszyka</a>
    </form>
        </div>
        {/block}
        

        {block name='product_reviews'}
          {hook h='displayProductListReviews' product=$product}
        {/block}
      </div>

      {include file='catalog/_partials/product-flags.tpl'}
    </div>
  </article>
</div>
{/block}

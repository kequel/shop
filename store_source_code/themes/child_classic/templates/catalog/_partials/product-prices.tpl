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
{if $product.show_price}
  <div class="product-prices">
    
    {block name='product_price'}
      <div
        class="product-price h5 {if $product.has_discount}has-discount{/if}">
        {if $product.has_discount}
            {if $product.discount_type === 'percentage'}
              <span class="discount discount-percentage" style="    TEXT-ALIGN: CENTER;
    font-weight: normal !important;
    background-color: #12c212 !important;
    color: white !important;
    font-size: 20px;
    width:300px;
    margin:0 !important;
    height: 40px; 
    padding-top:10px !important ">
    {l s='-%percentage% PROMOCJA' d='Shop.Theme.Catalog' sprintf=['%percentage%' => $product.discount_percentage_absolute]}</span>
            {else}
              <span class="discount discount-amount">
                  {l s='Save %amount%' d='Shop.Theme.Catalog' sprintf=['%amount%' => $product.discount_to_display]}
              </span>
            {/if}
          {/if}

        <div class="current-price">
          <span class='current-price-value' content="{$product.rounded_display_price}">
            {capture name='custom_price'}{hook h='displayProductPriceBlock' product=$product type='custom_price' hook_origin='product_sheet'}{/capture}
            {if '' !== $smarty.capture.custom_price}
              {$smarty.capture.custom_price nofilter}
            {else}
            {if $product.has_discount}
            <span class="znizka"> {($product.regular_price_amount / ($product.price_amount / $product.price_tax_exc))|number_format:2:'.':''} zł</span>
            {/if}
            <span class="cena_n">{$product.price_tax_exc|number_format:2:'.':' '} zł</span><span class="net-brut"> netto</span>
              <div class="product-prices js-product-prices">

              {if $product.has_discount}
             
                <span class="znizka">{$product.regular_price}</span>
     
              {/if}

              <span class="cena_n">{$product.price}</span><span class="net-brut"> brutto</span>
            </div>
            {/if}
          </span>
        </div>
        <div class="za_szt">
          Cena netto za sztukę: {$product.price_tax_exc|number_format:2:'.':' '} zł
        </div>
        <div class="najnizsza">
        Najniższa cena w ciągu 30 dni: <span id="cena_naj">{$product.price}</span> brutto 
        </div>

        {block name='product_unit_price'}
          {if $displayUnitPrice}
            <p class="product-unit-price sub">{l s='(%unit_price%)' d='Shop.Theme.Catalog' sprintf=['%unit_price%' => $product.unit_price_full]}</p>
          {/if}
        {/block}
      </div>
    {/block}

    {block name='product_without_taxes'}
      {if $priceDisplay == 2}
        <p class="product-without-taxes">{l s='%price% tax excl.' d='Shop.Theme.Catalog' sprintf=['%price%' => $product.price_tax_exc]}</p>
      {/if}
    {/block}

    {block name='product_pack_price'}
      {if $displayPackPrice}
        <p class="product-pack-price"><span>{l s='Instead of %price%' d='Shop.Theme.Catalog' sprintf=['%price%' => $noPackPrice]}</span></p>
      {/if}
    {/block}

    {block name='product_ecotax'}
      {if $product.ecotax.amount > 0}
        <p id="" class="price-ecotax">{l s='Including %amount% for ecotax' d='Shop.Theme.Catalog' sprintf=['%amount%' => $product.ecotax.value]}
          {if $product.has_discount}
            {l s='(not impacted by the discount)' d='Shop.Theme.Catalog'}
          {/if}
        </p>
      {/if}
    {/block}

    {hook h='displayProductPriceBlock' product=$product type="weight" hook_origin='product_sheet'}

  </div>
{/if}
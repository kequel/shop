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
<div class="product-add-to-cart js-product-add-to-cart">
  {if !$configuration.is_catalog}
    

    {block name='product_quantity'}
      <div class="product-quantity clearfix"
        style= " 
        display: flex;
        flex-direction: column; 
        align-items: flex-start;
        
        " 
        > 
        <div class="qty" style="line-height: 0;    margin-left: 75px;">
          <span id="product-availability2" class="product-available"  >
            <i class="fa fa-check" title="Produkt dostępny" style="color: #fff !important;"></i>
				  </span>
          <span style="font-size: 20px; margin-left:5px;color: #0050a7 !important;    margin-top: 15px;">ILOŚĆ</span>
          
          <div id="plusminus" style="display:inline-block; float:left;"> 
                <button style=" display:inline-block; margin-top:5px; padding: 2.5px 5px; background: #fff !important;" type="button" id="sub" class="sub"><span class="quantity-minus fa fa-minus-square" style="color: #0050a7 !important;"></span></button>
                <input style=" font-size:20px !important; color:#0050a7 !important;  display:inline-block; width:22px;    display: inline-block;height: 33px; padding: 2px 0px; text-align: center;" type="" name="qty" value="1" min="1" data-button-action="add-to-cart">
                <button style="display:inline-block;margin-top:5px; padding: 2.5px 5px; background: #fff !important;" type="button" id="add" class="add"><span class="quantity-minus fa fa-plus-square" style="color: #0050a7 !important;"></span></button>
              </div>
        </div>

        <div class="add_to_cart">
          <button
            class="btn btn-primary add-to-cart"
            data-button-action="add-to-cart"
            type="submit"
            style="min-width: 0px;
            
    font-size: 18px;

    width: 300px;
	  background-color:green;
    height: 50px;
    display: inline-block;    float: none;
    margin: 10px 0 0 0;
    color: #fff !important;
    font-weight: 400;"
            
          >
            <i class="fa fa-shopping-cart" style=" font-size: 12px;color: #fff !important"></i>
            Dodaj do koszyka
          </button>
        </div>

        {hook h='displayProductActions' product=$product}
      </div>
    {/block}
    <a href="tel:556463152" style="color:white; line-height:22px;"><p class="contact-info phone button" title="55 646 31 52" style="margin-top: 10px !important;  width: 300px;background-color: #003169 !important; color:white !important;
    text-align: center; width=300px; display: block;  margin: 0 0 10px 0; line-height: normal; font-size:18px; color:white; float:left; padding: 0px 0px 5px 0px; max-width:auto; max-width: inherit;">
        <i class="fa fa-phone" style=" background-color: #003169 !important; color:white !important; padding-top: 10px;"></i> lub zamów telefonicznie<br> 55 646 31 52
    </p> </a>

    {block name='product_availability'}
      <span id="product-availability" class="js-product-availability">
        {if $product.show_availability && $product.availability_message}
          {if $product.availability == 'available'}
            <i class="material-icons rtl-no-flip product-available">&#xE5CA;</i>
          {elseif $product.availability == 'last_remaining_items'}
            <i class="material-icons product-last-items">&#xE002;</i>
          {else}
            <i class="material-icons product-unavailable">&#xE14B;</i>
          {/if}
          {$product.availability_message}
        {/if}
      </span>
    {/block}

    {block name='product_minimal_quantity'}
      <p class="product-minimal-quantity js-product-minimal-quantity">
        {if $product.minimal_quantity > 1}
          {l
          s='The minimum purchase order quantity for the product is %quantity%.'
          d='Shop.Theme.Checkout'
          sprintf=['%quantity%' => $product.minimal_quantity]
          }
        {/if}
      </p>
    {/block}
  {/if}
</div>

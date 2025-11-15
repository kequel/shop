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
{extends file=$layout}

{block name='content'}

  <section id="main">
    <div class="cart-grid row">

      <!-- Left Block: cart product informations & shpping -->
      <div id="lewy_kosz" class="cart-grid-body col-xs-12 col-lg-8">

        <!-- cart products detailed -->
        <div class="card cart-container">
          <div class="card-block">
            <h1 class="h1" style="font-size: 24px; font-weight:700 !important">{l s='Shopping Cart' d='Shop.Theme.Checkout'}</h1>
          </div>
          <hr class="separator">
           <div class="cart-row cart-row-head" style="    border-bottom: 1px solid #e0e9f3;margin-top:20px; height:25px">
        <div class="cart-col-1" style="float:left; color: #808080 !important">
          Produkty
        </div>
        <div class="cart-col-2"style="float:left; color: #808080 !important; padding-left:350px; padding">
          Cena
        </div>
        <div class="cart-col-3"style="float:left; color: #808080 !important; padding-left:150px;">
          Ilość
        </div>
        <div class="cart-col-4"style="float:left; color: #808080 !important;padding-left:150px;">
          Suma
        </div>
        <div class="cart-col-5"style="float:left; color: #808080 !important"></div>
      </div>
<br>
          {block name='cart_overview'}
            {include file='checkout/_partials/cart-detailed.tpl' cart=$cart}
          {/block}

     
        </div>
         {if !$customer.is_logged}
        <div class="zaloz_konto" style="border: 1px solid #e0e9f3;line-height: 32px; padding: 15px; color: #203461; margin-bottom: 20px;">
		  <div class="zakladajac_konto">
			<strong>Zakładając konto w MOP SERWIS zyskujesz:</strong>
			  <ul>
				<li>Szybki proces zamawiania</li>
				<li>Pełna historia wszystkich zamówień</li>
				<li>Dostęp do specjalnych promocji</li>
			  </ul>
		  </div>
		  <div class="zarejestruj_sie">
			  <a href="http://localhost:8080/login?create_account=1" data-link-action="display-register-form" class="button">Zarejestruj się</a>
		  </div>
	  </div>
   {/if}
    



        <!-- shipping informations -->
        {block name='hook_shopping_cart_footer'}
          {hook h='displayShoppingCartFooter'}
        {/block}
      </div>

      <!-- Right Block: cart subtotal & cart total -->
     {block name='cart_voucher'}
    {include file='checkout/_partials/cart-voucher.tpl'}
  {/block}
        {block name='cart_summary'}
          <div id="podsumowanie" class="card cart-summary">

            {block name='hook_shopping_cart'}
              {hook h='displayShoppingCart'}
            {/block}

            {block name='cart_totals'}
              {include file='checkout/_partials/cart-detailed-totals.tpl' cart=$cart}
            {/block}

            {block name='cart_actions'}
              {include file='checkout/_partials/cart-detailed-actions.tpl' cart=$cart}
            {/block}

          </div>
        {/block}

           {block name='continue_shopping'}
          <a id="kontynuuj" class="label" href="{$urls.pages.index}">
           {l s='Continue shopping' d='Shop.Theme.Actions'}
          </a>
        {/block}

      </div>

    </div>
  </section>
{/block}

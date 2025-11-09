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
{extends file='page.tpl'}

{block name='page_title'}
  <span id="nagl_zal">ZALOGUJ SIĘ NA SWOJE KONTO</span>
{/block}

{block name='page_content'}
    {block name='login_form_container'}
      <section class="login-form">
        {render file='customer/_partials/login-form.tpl' ui=$login_form}
      </section>
  
      {block name='display_after_login_form'}
        {hook h='displayCustomerLoginFormAfter'}
      {/block}
      <div class="no-account" id="nima">

      {if isset($page.page_name) && $page.page_name == 'authentication'}
      <div id="text_nima">
      <h1 id="napis_nima">Nie masz konta? Zarejestruj się</h1>
      <p id="opis_nima">Dzięki utworzeniu konta będziesz mógł robić zakupy, śledzić status zamówień i przeglądać historie zakupów</p>
      </div>
      <a id="guzik_nima" href="{$urls.pages.register}" data-link-action="display-register-form">
          Zarejestruj się
        </a>
      {else}
        <a href="{$urls.pages.register}" data-link-action="display-register-form">
          {l s='No account? Create one here' d='Shop.Theme.Customeraccount'}
        </a>
        {/if}
      </div>
    {/block}
{/block}

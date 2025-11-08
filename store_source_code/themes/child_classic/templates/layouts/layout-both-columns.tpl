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

{include file='_partials/helpers.tpl'}

<!doctype html>
<html lang="{$language.locale}">

  <head>
    {block name='head'}
      {include file='_partials/head.tpl'}
    {/block}
  </head>

  <body id="{$page.page_name}" class="{$page.body_classes|classnames}">

    {block name='hook_after_body_opening_tag'}
      {hook h='displayAfterBodyOpeningTag'}
    {/block}

    <main>
      {block name='product_activation'}
        {include file='catalog/_partials/product-activation.tpl'}
      {/block}

      <header id="header">
        {block name='header'}
          {include file='_partials/header.tpl'}
        {/block}
      </header>

      {if isset($page.page_name) && ($page.page_name == 'category' || $page.page_name == 'index'|| $page.page_name == 'product' ||$page.page_name == 'checkout'  )}
      
      <section id="wrapper">
      {else}
      <section id="wrapper2">
      {/if}

       
        {block name='notifications'}
          {include file='_partials/notifications.tpl'}
        {/block}
        
         {if isset($page.page_name) && $page.page_name != 'checkout' }
      
        <div id="kategorie">
        
          {hook h="displayWrapperTop"}
        </div>
        {/if}
        <div class="container">
          {block name='breadcrumb'}
            {include file='_partials/breadcrumb.tpl'}
          {/block}

          {block name="left_column"}
            <div id="left-column" class="col-xs-12 col-sm-4 col-md-3">
              {if $page.page_name == 'product'}
                {hook h='displayLeftColumnProduct'}
              {else}
                {hook h="displayLeftColumn"}
              {/if}
            </div>
          {/block}

          {block name="content_wrapper"}
            <div id="content-wrapper" class="js-content-wrapper left-column right-column col-sm-4 col-md-6">
              {hook h="displayContentWrapperTop"}
              {block name="content"}
                <p>Hello world! This is HTML5 Boilerplate.</p>
              {/block}
              {hook h="displayContentWrapperBottom"}
            </div>
          {/block}

          {block name="right_column"}
            <div id="right-column" class="col-xs-12 col-sm-4 col-md-3">
              {if $page.page_name == 'product'}
                {hook h='displayRightColumnProduct'}
              {else}
                {hook h="displayRightColumn"}
              {/if}
            </div>
          {/block}
        </div>
        {hook h="displayWrapperBottom"}
      </section>

      <footer id="footer" class="js-footer"
      {if isset($page.page_name) && $page.page_name == 'category'}
      style="margin-top:400px !important;"
      {/if}
      {if isset($page.page_name) &&  $page.page_name == 'product'}
      style="margin-top:100px !important;"
      {/if}
      
      >
        <div class="footer-top-bar">
    <div class="container2">
        <div class="footer-boxes1">
            <h6>MOP SERWIS</h6>
            <p>
                NIP: 581-192-37-64<br>
                KRS: 0000324556<br>
                REGON: 220761326<br>
                ING Bank Śląski<br>
                98 1050 1764 1000 0090 8115 9049
            </p>
        </div>

        <div class="footer-boxes1">
            <h6>Dane teleadresowe</h6>
            <ul>
                <li><i class="fa fa-map-marker"></i><span>ul. Ogrodowa 14, 82-500 Kwidzyn</span></li>
                <li><i class="fa fa-phone"></i><span><a href="tel:55 646 31 52">55 646 31 52</a></span></li>
                <li><i class="fa fa-envelope"></i><a href="mailto:esklep@mopserwis.pl">esklep@mopserwis.pl</a></li>
                <li><i class="fa-brands fa-facebook-f"></i><a href="https://www.facebook.com/Mopserwis/" target="_blank">facebook.com</a></li>
                <li><i class="fa-brands fa-linkedin"></i><a href="https://www.linkedin.com/company/35653510" target="_blank">linkedin.com</a></li>
                <li><i class="fa-brands fa-instagram"></i><a href="https://www.instagram.com/mopserwis/" target="_blank">instagram.com</a></li>
                <li><i class="fa-brands fa-google"></i><a href="https://www.google.com/shopping/customerreviews/merchantreviews?q=mopserwis.pl" target="_blank">Opinie w Google</a></li>
            </ul>
        </div>

        <div class="footer-boxes">
            <h6>Informacje</h6>
            <ul>
                <li><a href="http://localhost:8080/content/4-about-us">Dlaczego Mop Serwis</a></li>
                <li><a href="http://localhost:8080/content/3-terms-and-conditions-of-use">Regulamin zakupów</a></li>
                <li><a href="http://localhost:8080/content/2-legal-notice">Polityka prywatności</a></li>
                <li><a href="http://localhost:8080/contact-us">Kontakt</a></li>
            </ul>
        </div>

        <div class="footer-boxes">
            <h6>Twoje zamówienie</h6>
            <ul>
                <li><a href="http://localhost:8080/content/6-zwroty">Zwroty towarów</a></li>
                <li><a href="http://localhost:8080/content/7-reklamacje">Reklamacje</a></li>
            </ul>
        </div>

        <div class="footer-boxes">
            <h6>Zamówienia</h6>
            <ul>
                <li><a href="http://localhost:8080/content/5-secure-payment">Płatności</a></li>
                <li><a href="http://localhost:8080/content/1-delivery">Koszty dostawy</a></li>
            </ul>
        </div>
    </div>
</div>
<div class="copyrights">
  
        <a href="https://mopserwis.pl/">© 2025 MOP SERWIS</a> <span>| All Rights Reserved</span>
    
</div>
      </footer>

    </main>

    {block name='javascript_bottom'}
      {include file="_partials/javascript.tpl" javascript=$javascript.bottom}
    {/block}

    {block name='hook_before_body_closing_tag'}
      {hook h='displayBeforeBodyClosingTag'}
    {/block}
  </body>

</html>

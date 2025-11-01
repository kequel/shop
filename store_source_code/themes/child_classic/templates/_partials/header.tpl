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
{block name='header_banner'}
  <div class="header-banner">
    {hook h='displayBanner'}
  </div>
{/block}

{block name='header_nav'}
  <nav class="header-nav">
    <div class="container">
      <div class="row">
      <div class="col-md-6">
        <a class="header-nav-phone" href="tel:556463152">55 646 31 52</a>
        <a class="header-nav-mail" href="mailto:esklep@mopserwis.pl">esklep@mopserwis.pl</a>
        <a style="padding: 0 10px; color:white; margin-left: 25px"> Darmowa dostawa od 280zł netto</a> 
      </div>  
      <div class="col-md-6 text-xs-right"> 
  <style type="text/css">
	.platforma_b2b{
	/* display:none; */
	}
	.platforma_b2b a {
	border: 1px solid white; 
	padding: 0px 13px; 
	border-radius: 5px; 
	margin: 0px 15px; 
	color: white;
	}
	.platforma_b2b a:hover {
	background-color:white;
	color: #003169;
	}
  </style>
   <!-- <a  style="padding: 0 10px;    border: 1px solid white;    margin-right: 15px" href="https://docs.google.com/forms/d/e/1FAIpQLSd9NVP8Z1EXH75CtdZA4wP6qpuGZQIsVhEHb1H0QHlVltebzg/viewform?vc=0&c=0&w=1&flr=0" target="_blank">Darmowa wycena dla Ciebie </a> -->
  <span class="platforma_b2b"><a href="https://biznes.mopserwis.pl/?_gl=1*4zbu73*_gcl_au*NjQwMjY5NjM4LjE3NjEyMTEwOTI.*_ga*NDE4NTE4MTMuMTc2MTIxMTA3Mg..*_ga_ML1KDEQRE5*czE3NjE0OTEyNzckbzQkZzEkdDE3NjE0OTM5ODIkajU5JGwwJGgxMTI5Mzk0MDM1JGROazdCX3IzZHgzWEwxdDBrMEdPNzBzLVctbWVTVnNpaXNB" target="_blank">Platforma b2b / Klienci Biznesowi</a></span>
  </span>
  
  <a class="OpinieGoogleHeader" style="margin-right: 17px; margin-left:4px;" href="https://www.google.com/shopping/customerreviews/merchantreviews?q=mopserwis.pl" target="_blank">
      Nasze opinie w Google
    </a>

    <div class="col-md-5 col-xs-12">
            {hook h='displayNav1'}
          </div>
  </div>
        
      </div>
    </div>
  </nav>
{/block}

{block name='header_top'}
  <div class="header-top">
 
        <div class="hidden-md-up text-sm-center mobile">
          <div class="float-xs-left" id="menu-icon">
            <i class="material-icons d-inline">&#xE5D2;</i>
          </div>
          <div class="float-xs-right" id="_mobile_cart"></div>
          <div class="float-xs-right" id="_mobile_user_info"></div>
          <div class="top-logo" id="_mobile_logo"></div>
          <div class="clearfix"></div>
        </div>
    <div class="container">
       <div class="row">
        <div class="col-md-2 hidden-sm-down" id="_desktop_logo">
          {if $shop.logo_details}
            {if $page.page_name == 'index'}
              <h1>
                {renderLogo}

              </h1>
            {else}
              {renderLogo}
            
            {/if}
          {/if}
          
        </div>
        <div class="naj"><strong>NAJLEPSZY DOSTAWCA</strong><br>PAPIERÓW HIGIENICZNYCH </div>
        <div class="header-top-right col-md-10 col-sm-12 position-static">
          
          {hook h='displayTop'}
          
        </div>
        <div class="hidden-sm-down">
          <div class="col-md-7 right-nav">
              {hook h='displayNav2'}
              
          </div>
        </div>
      </div>
      <div id="mobile_top_menu_wrapper" class="row hidden-md-up" style="display:none;">
        <div class="js-top-menu mobile" id="_mobile_top_menu"></div>
        <div class="js-top-menu-bottom">
          <div id="_mobile_currency_selector"></div>
          <div id="_mobile_language_selector"></div>
          <div id="_mobile_contact_link"></div>
        </div>
      </div>
    </div>
  </div>
  {hook h='displayNavFullWidth'}
{/block}

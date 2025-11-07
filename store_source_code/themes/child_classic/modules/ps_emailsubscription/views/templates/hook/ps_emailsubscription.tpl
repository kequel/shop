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
      {if isset($page.page_name) && ($page.page_name == 'category' || $page.page_name == 'product')}
    <div class="aside-box aside-contact-box">
    <img src="http://localhost:8080/themes/child_classic/assets/aside-contact-img.png" alt="Kontakt z nami">
    <h6>Potrzebujesz pomocy?</h6>
    <p>Skontaktuj się z nami!</p>
    <a href="https://mopserwis.pl/kontakt" class="button btn">Kontakt</a>
</div>
    {/if}
<div class="block_newsletter col-lg-8 col-md-12 col-sm-12" id="blockEmailSubscription_{$hookName}">

  <div class="row" id="news_col">
  
    <h1 id="newsletter">NEWSLETTER</h1>
    <p id="zapisz">Zapisz się do naszego Newsletter'a</p>
    <div class="col-md-7 col-xs-12">
      <form action="{$urls.current_url}#blockEmailSubscription_{$hookName}" method="post">
        <div class="row">
          <div class="col-xs-12">
           
            <div class="input-wrapper">
              <input
              id="news_input"
                name="email"
                type="email"
                value="{$value}"
                placeholder="{l s='Your email address' d='Shop.Forms.Labels'}"
                aria-labelledby="block-newsletter-label"
                required
              >
            </div>
            <div id="check_news">
            <input type="checkbox" name="agreement[4]" id="agreement_4" value="1" required="required">
            <label for="agreement_4">
            Zapoznaj się z zasadami ochrony danych osobowych dostępnymi w&nbsp;<a id="linknews" href="https://mopserwis.pl/content/8-polityka-prywatnosci">Polityce Prywatności</a>. Masz prawo w każdym czasie cofnąć swoją zgodę na przetwarzanie swoich danych na stronie sklepu - esklep@mopserwis.pl.
            <span id="zap">(wymagana)</span>        </label>
            </div>
             <input
             id="subskrybuj"
              class="btn btn-primary float-xs-right hidden-xs-down"
              name="submitNewsletter"
              type="submit"
              
              value="{l s='Subscribe' d='Shop.Theme.Actions'}"
            >
            <input
              class="btn btn-primary float-xs-right hidden-sm-up"
              name="submitNewsletter"
              type="submit"
              value="{l s='OK' d='Shop.Theme.Actions'}"
            >
            <input type="hidden" name="blockHookName" value="{$hookName}" />
            <input type="hidden" name="action" value="0">
            <div class="clearfix"></div>
          </div>
          <div class="col-xs-12">
             
              {if $msg}
                <p class="alert {if $nw_error}alert-danger{else}alert-success{/if}">
                  {$msg}
                </p>
              {/if}
              {hook h='displayNewsletterRegistration'}
              {if isset($id_module)}
                {hook h='displayGDPRConsent' id_module=$id_module}
              {/if}
          </div>

          </div>

        </div>
      </form>
    </div>
  </div>


</div>

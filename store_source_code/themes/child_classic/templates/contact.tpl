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

{block name='page_header_container'}{/block}

{* Usuwamy kolumny boczne *}
{block name="left_column"}{/block}
{block name="right_column"}{/block}

{block name='page_content'}
  <div class="contact-page-wrapper">
    {* Standardowy widget formularza kontaktowego *}
    {widget name="contactform"}
    
    {* Sekcja z listą pracowników - dodana poniżej formularza *}
    <div class="contact-person-list-wrap">
      
      {* DZIAŁ 1: BIURO OBSŁUGI KLIENTA *}
      <div class="dzial-row">
        <div class="nazwa_dzialu">BIURO OBSŁUGI KLIENTA</div>
        <div class="dzial-kontakty">
          <div class="kontakt-dane-osobowe">
            <h5>Ania</h5>
            <p class="person-phone">
              <i class="fa fa-phone"></i>
              <a href="tel:721590132">721 590 132</a>
            </p>
            <a href="mailto:ANIA@mopserwis.pl" class="person-email">
              <i class="fa fa-envelope"></i>
              <span>Wyślij e-mail</span>
            </a>
          </div>

          <div class="kontakt-dane-osobowe">
            <h5>Natalia</h5>
            <p class="person-phone">
              <i class="fa fa-phone"></i>
              <a href="tel:607364422">607 364 422</a>
            </p>
            <a href="mailto:NATALIA@mopserwis.pl" class="person-email">
              <i class="fa fa-envelope"></i>
              <span>Wyślij e-mail</span>
            </a>
          </div>

          <div class="kontakt-dane-osobowe">
            <h5>Paulina</h5>
            <p class="person-phone">
              <i class="fa fa-phone"></i>
              <a href="tel:794210400">794 210 400</a>
            </p>
            <a href="mailto:PAULINA@mopserwis.pl" class="person-email">
              <i class="fa fa-envelope"></i>
              <span>Wyślij e-mail</span>
            </a>
          </div>
        </div>
      </div>

      {* DZIAŁ 2: DYSTRYBUCJA / HURTOWNIE *}
      <div class="dzial-row">
        <div class="nazwa_dzialu">DYSTRYBUCJA / HURTOWNIE</div>
        <div class="dzial-kontakty">
          <div class="kontakt-dane-osobowe">
            <h5>Anna Kisa</h5>
            <p class="person-phone">
              <i class="fa fa-phone"></i>
              <a href="tel:605618973">605 618 973</a>
            </p>
            <a href="mailto:ANNA.KISA@mopserwis.pl" class="person-email">
              <i class="fa fa-envelope"></i>
              <span>Wyślij e-mail</span>
            </a>
          </div>
        </div>
      </div>

      {* DZIAŁ 3: DZIAŁ DS. OBSŁUGI KLIENTÓW BIZNESOWYCH *}
      <div class="dzial-row">
        <div class="nazwa_dzialu">DZIAŁ DS. OBSŁUGI KLIENTÓW BIZNESOWYCH</div>
        <div class="dzial-kontakty">
          <div class="kontakt-dane-osobowe">
            <h5>Agnieszka Nogowska</h5>
            <p class="stanowisko">Specjalista ds. obsługi B2B</p>
            <p class="person-phone">
              <i class="fa fa-phone"></i>
              <a href="tel:605271030">605 271 030</a>
            </p>
            <a href="mailto:agnieszka.nogowska@mopserwis.pl" class="person-email">
              <i class="fa fa-envelope"></i>
              <span>agnieszka.nogowska@mopserwis.pl</span>
            </a>
          </div>

          <div class="kontakt-dane-osobowe">
            <h5>Barbara Danielewicz</h5>
            <p class="stanowisko">Specjalista ds. obsługi B2B</p>
            <p class="person-phone">
              <i class="fa fa-phone"></i>
              <a href="tel:609905200">609 905 200</a>
            </p>
            <a href="mailto:barbara.danielewicz@mopserwis.pl" class="person-email">
              <i class="fa fa-envelope"></i>
              <span>barbara.danielewicz@mopserwis.pl</span>
            </a>
          </div>

          <div class="kontakt-dane-osobowe">
            <h5>Monika Głowacka</h5>
            <p class="stanowisko">Specjalista ds. obsługi B2B</p>
            <p class="person-phone">
              <i class="fa fa-phone"></i>
              <a href="tel:607691814">607 691 814</a>
            </p>
            <a href="mailto:monika.glowacka@mopserwis.pl" class="person-email">
              <i class="fa fa-envelope"></i>
              <span>monika.glowacka@mopserwis.pl</span>
            </a>
          </div>
        </div>
      </div>

    </div>
  </div>
{/block}

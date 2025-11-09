{*
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
<div class="images-container js-images-container">

  {block name='product_cover'}
    {* Zmieniamy product_cover na karuzelę głównych zdjęć *}
    <div id="product-cover-carousel" data-ride="carousel" class="carousel slide product-cover" data-interval="false" data-wrap="true" data-pause="false" data-touch="true">
      <div class="carousel-inner" role="listbox" aria-label="{l s='Product images carousel' d='Shop.Theme.Global'}">
        {foreach from=$product.images item=image name='product_cover_slides'}
          <div id="karuzela_xd" class="carousel-item {if $smarty.foreach.product_cover_slides.first}active{/if}" role="option" aria-hidden="{if $smarty.foreach.product_cover_slides.first}false{else}true{/if}">
            <img
            id="zdj_pr"
              class="js-qv-product-cover img-fluid"
              src="{$image.bySize.large_default.url}" {* Używamy bySize.large_default dla głównego zdjęcia *}
              {if !empty($image.legend)}
                alt="{$image.legend}"
                title="{$image.legend}"
              {else}
                alt="{$product.name}"
              {/if}
              loading="lazy"
            >
          
          </div>
        {foreachelse}
          <div class="carousel-item active">
            <img
              class="img-fluid"
              src="{$urls.no_picture_image.bySize.medium_default.url}"
              loading="lazy"
              width="{$urls.no_picture_image.bySize.medium_default.width}"
              height="{$urls.no_picture_image.bySize.medium_default.height}"
            >
          </div>
        {/foreach}
      </div>

      {* Kontrolki nawigacyjne (strzałki) dla głównego slidera *}
      <div class="direction" aria-label="{l s='Carousel buttons' d='Shop.Theme.Global'}">
        <a class="left carousel-control" href="#product-cover-carousel" role="button" data-slide="prev" aria-label="{l s='Previous' d='Shop.Theme.Global'}">
          <span id="lewo_prod" class="icon-prev" aria-hidden="true">
            <i id="lewo3" class="fa fa-angle-left"></i>
          </span>
        </a>
        <a class="right carousel-control" href="#product-cover-carousel" role="button" data-slide="next" aria-label="{l s='Next' d='Shop.Theme.Global'}">
          <span id="prawo_prod" class="icon-next" aria-hidden="true">
            <i id="prawo3" class="fa fa-angle-right"></i>
          </span>
        </a>
      </div>

    </div>
  {/block}
  {block name='product_images'}

    <div class="js-qv-mask mask">

      <ul class="product-images js-qv-product-images">

        {foreach from=$product.images item=image}


          <li class="thumb-container js-thumb-container">

            <img

              class="thumb js-thumb {if $image.id_image == $product.default_image.id_image} selected js-thumb-selected {/if}"

              data-image-medium-src="{$image.bySize.medium_default.url}"

              data-image-large-src="{$image.bySize.large_default.url}"

              src="{$image.bySize.small_default.url}"

              {if !empty($image.legend)}

                alt="{$image.legend}"

                title="{$image.legend}"

              {else}

                alt="{$product.name}"

              {/if}

              loading="lazy"

              width="{$product.default_image.bySize.small_default.width}"

              height="{$product.default_image.bySize.small_default.height}"

            >

          </li>

        {/foreach}

      </ul>

    </div>

  {/block}
  
<script></script>
{hook h='displayAfterProductThumbs' product=$product}

</div>
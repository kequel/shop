{extends "customer/_partials/customer-form.tpl"}

{block "form_field"}
  {* Renderujemy tylko pola, które mają pozostać, ORAZ obowiązkowe zgody, które są potrzebne, by PrestaShop działał. *}
  {if $field.name === 'firstname' || $field.name === 'lastname' || $field.name === 'email' || $field.name === 'newsletter' || $field.name === 'customer_privacy' || $field.name === 'psgdpr'}
    {$smarty.block.parent}
  {/if}
{/block}

{block "form_buttons"}
    <button
      class="continue btn btn-primary float-xs-right"
      name="continue"
      data-link-action="register-new-customer"
      type="submit"
      value="1"
    >
        {l s='Continue' d='Shop.Theme.Actions'}
    </button>
{/block}
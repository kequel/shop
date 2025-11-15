{**
 * Custom Contact Form Template
 *}

<section class="contact-form">
<h2 class="contact-main-title">Kontakt z nami</h2>
  
  <form action="{$urls.pages.contact}" method="post" enctype="multipart/form-data">

    {if $notifications}
      <div class="alert {if $notifications.nw_error}alert-danger{else}alert-success{/if}">
        <ul>
          {foreach $notifications.messages as $notif}
            <li>{$notif}</li>
          {/foreach}
        </ul>
      </div>
    {/if}

    <section class="form-fields">
      
      <div class="form-group row">
        <label class="col-md-3 form-control-label">Temat</label>
        <div class="col-md-9">
          {if isset($contact.contacts) && $contact.contacts}
            <select name="id_contact" id="id_contact" class="form-control form-control-select">
              {foreach $contact.contacts as $contact_elt}
                <option value="{$contact_elt.id_contact}" {if isset($contact.id_contact) && $contact.id_contact == $contact_elt.id_contact}selected{/if}>
                  {$contact_elt.name}
                </option>
              {/foreach}
            </select>
          {/if}
        </div>
      </div>
      
      <div class="form-group row">
        <label class="col-md-3 form-control-label">Adres e-mail</label>
        <div class="col-md-9">
          <input
            class="form-control"
            name="from"
            type="email"
            value="{if isset($contact.email)}{$contact.email}{/if}"
            placeholder="twój@email.com"
            required
          >
        </div>
      </div>
      
      <div class="form-group row">
        <label class="col-md-3 form-control-label">Wiadomość</label>
        <div class="col-md-9">
          <textarea
            class="form-control"
            name="message"
            rows="3"
            placeholder="Jak możemy pomóc?"
            required
          >{if isset($contact.message)}{$contact.message}{/if}</textarea>
        </div>
      </div>

      {* RODO Checkbox *}
      <div class="form-group row">
        <div class="col-md-12">
          <div class="custom-checkbox-wrapper">
            <input type="checkbox" name="gdpr_consent" id="gdpr_consent" class="rodo-checkbox" value="1" required>
            <label for="gdpr_consent">
              Zapoznaj się z zasadami ochrony danych osobowych dostępnymi w 
              <a href="{url entity='cms' id='3'}" target="_blank">Polityce Prywatności</a>. 
              Masz prawo w każdym czasie cofnąć swoją zgodę na przetwarzanie swoich danych na stronie sklepu - esklep@mopserwis.pl. (wymagana)
            </label>
          </div>
        </div>
      </div>
    </section>

    <footer class="form-footer">
      <input type="hidden" name="url" value="{if isset($smarty.server.HTTP_REFERER)}{$smarty.server.HTTP_REFERER}{/if}" />
      <input type="hidden" name="token" value="{if isset($token)}{$token}{/if}" />
      <button class="btn btn-primary btn-wyslij-button" type="submit" name="submitMessage">
        WYŚLIJ
      </button>
    </footer>
  </form>
</section>

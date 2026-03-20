import re

with open('public/index.html', 'r') as f:
    html = f.read()

# FIX 1: rimuovi margin-top negativo che causa overlap
html = html.replace('margin-top: -22px', 'margin-top: 8px')
html = html.replace('margin-top:-22px', 'margin-top:8px')

# FIX 3: VIES loading - aggiungi testo stato sotto lo spinner
old_spinner = '<div class="piva-spinner" id="piva-spinner"></div>'
new_spinner = '''<div class="piva-spinner" id="piva-spinner"></div>
        <div id="vies-loading-text" style="display:none;font-size:11px;color:#0d6fa8;margin-top:6px;display:none;align-items:center;gap:6px;">
          <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="#0d6fa8" stroke-width="2.5" stroke-linecap="round"><path d="M21 12a9 9 0 1 1-6.219-8.56"/></svg>
          Verifica P.IVA in corso sul registro VIES europeo...
        </div>'''
html = html.replace(old_spinner, new_spinner)

# FIX 3: mostra/nascondi testo loading nella funzione lookupPIVA
html = html.replace(
    "spin.style.display='block';",
    "spin.style.display='block';\n    var lt=document.getElementById('vies-loading-text');if(lt){lt.style.display='flex';}"
)
html = html.replace(
    "spin.style.display='none';",
    "spin.style.display='none';\n      var lt=document.getElementById('vies-loading-text');if(lt){lt.style.display='none';}"
)

# FIX 2: validazione campi obbligatori per ogni step
old_goto = "function goTo(s){"
new_goto = """function validateStep(s){
  if(s===1){
    if(!document.getElementById('f-corso').value){
      alert('Seleziona un corso per continuare.');return false;
    }
  }
  if(s===2){
    var nome=document.getElementById('f-nome').value.trim();
    var cognome=document.getElementById('f-cognome').value.trim();
    var email=document.getElementById('f-email').value.trim();
    var tel=document.getElementById('f-tel').value.trim();
    var ruolo=document.getElementById('f-ruolo').value;
    if(!nome||!cognome){alert('Inserisci nome e cognome.');return false;}
    if(!email||!email.includes('@')){alert('Inserisci un indirizzo email valido.');return false;}
    if(!tel){alert('Inserisci il numero di telefono.');return false;}
    if(!ruolo){alert('Seleziona il tuo profilo professionale.');return false;}
  }
  if(s===3){
    if(!currentType){alert('Seleziona il tipo di fatturazione.');return false;}
    if(currentType==='privato'){
      if(!document.getElementById('f-cf').value){alert('Inserisci il codice fiscale.');return false;}
      if(!document.getElementById('f-via').value){alert('Inserisci l\\'indirizzo di residenza.');return false;}
      if(!document.getElementById('f-cap').value){alert('Inserisci il CAP.');return false;}
    }
    if(currentType==='farmacia'){
      if(!document.getElementById('f-piva').value){alert('Inserisci la Partita IVA.');return false;}
    }
  }
  return true;
}
function goTo(s){"""

html = html.replace(old_goto, new_goto)

# FIX 2: aggiungi validazione ai bottoni Avanti
html = html.replace("onclick=\"goTo(2)\"", "onclick=\"if(validateStep(1))goTo(2)\"")
html = html.replace("onclick=\"goTo(3)\"", "onclick=\"if(validateStep(2))goTo(3)\"")
html = html.replace("onclick=\"goTo(4)\"", "onclick=\"if(validateStep(3))goTo(4)\"")

# FIX 4: icone premium per i corsi
old_compresse_icon = '''<symbol id="icon-compresse" viewBox="0 0 24 24" fill="none" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
      <ellipse cx="12" cy="12" rx="9" ry="5" transform="rotate(-40 12 12)"/>
      <line x1="7.5" y1="7.2" x2="16.5" y2="16.8" transform="rotate(-40 12 12)"/>
    </symbol>'''

new_compresse_icon = '''<symbol id="icon-compresse" viewBox="0 0 24 24" fill="none" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round">
      <rect x="3" y="9" width="18" height="6" rx="3"/>
      <line x1="12" y1="9" x2="12" y2="15"/>
      <circle cx="7.5" cy="12" r="1.2" fill="currentColor" stroke="none"/>
      <circle cx="16.5" cy="12" r="1.2" fill="currentColor" stroke="none"/>
      <path d="M6 7c0-1.1.9-2 2-2h8a2 2 0 0 1 2 2"/>
      <path d="M6 17c0 1.1.9 2 2 2h8a2 2 0 0 0 2-2"/>
    </symbol>'''

old_cannabis_icon = '''<symbol id="icon-cannabis" viewBox="0 0 24 24" fill="none" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
      <path d="M12 22v-7"/>
      <path d="M12 15C9 15 4 12 4 7c2 0 5 1 8 4 3-3 6-4 8-4 0 5-5 8-8 8z"/>
      <path d="M9 20h6"/>
    </symbol>'''

new_cannabis_icon = '''<symbol id="icon-cannabis" viewBox="0 0 24 24" fill="none" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round">
      <path d="M12 22v-6"/>
      <path d="M12 16c-2 0-6-1.5-7-5 1.5 0 4 .5 7 3 3-2.5 5.5-3 7-3-1 3.5-5 5-7 5z"/>
      <path d="M12 13C10.5 11 9 7.5 10 4c1 1.5 2 4 2 6 0-2 1-4.5 2-6 1 3.5-.5 7-2 9z"/>
      <path d="M10 20h4"/>
    </symbol>'''

html = html.replace(old_compresse_icon, new_compresse_icon)
html = html.replace(old_cannabis_icon, new_cannabis_icon)

with open('public/index.html', 'w') as f:
    f.write(html)

print("✅ Patch applicata con successo!")
print("   Fix 1: overlap barra progresso")
print("   Fix 2: validazione campi obbligatori")
print("   Fix 3: stato caricamento VIES")
print("   Fix 4: icone corsi aggiornate")

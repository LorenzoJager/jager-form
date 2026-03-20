with open('public/index.html', 'r') as f:
    html = f.read()

# Aggiungi stile bottone disabilitato
old_style = '.btn-next:hover{background:#0a5a8c;}'
new_style = '''.btn-next:hover{background:#0a5a8c;}
.btn-next:disabled{background:#b8c8d4;cursor:not-allowed;opacity:0.6;}
.btn-next:disabled:hover{background:#b8c8d4;}'''
html = html.replace(old_style, new_style)

# Step 1 - bottone Avanti disabilitato finche non selezioni corso
old_s1 = '''<input type="hidden" id="f-corso" value=""/>
      <div class="form-nav"><button class="btn-next" onclick="if(validateStep(1))goTo(2)">Avanti →</button></div>'''
new_s1 = '''<input type="hidden" id="f-corso" value=""/>
      <div class="form-nav"><button class="btn-next" id="btn-avanti-1" disabled onclick="goTo(2)">Avanti →</button></div>'''
html = html.replace(old_s1, new_s1)

# Aggiorna selectCourse per abilitare il bottone
old_select = "function selectCourse(val,id){"
new_select = """function selectCourse(val,id){
  var btn=document.getElementById('btn-avanti-1');
  if(btn)btn.disabled=false;"""
html = html.replace(old_select, new_select)

# Step 2 - bottone Avanti disabilitato finche non compili tutti i campi
old_s2_btn = 'onclick="if(validateStep(2))goTo(3)">Avanti →</button>'
new_s2_btn = 'id="btn-avanti-2" onclick="if(validateStep(2))goTo(3)">Avanti →</button>'
html = html.replace(old_s2_btn, new_s2_btn)

# Rimuovi i popup alert dalla validateStep e usa solo return false
old_validate = """function validateStep(s){
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
}"""

new_validate = """function checkStep2(){
  var nome=document.getElementById('f-nome').value.trim();
  var cognome=document.getElementById('f-cognome').value.trim();
  var email=document.getElementById('f-email').value.trim();
  var tel=document.getElementById('f-tel').value.trim();
  var ruolo=document.getElementById('f-ruolo').value;
  var ok=nome&&cognome&&email&&email.includes('@')&&tel&&ruolo;
  var btn=document.getElementById('btn-avanti-2');
  if(btn)btn.disabled=!ok;
}
function validateStep(s){
  if(s===3){
    if(!currentType)return false;
    if(currentType==='privato'){
      if(!document.getElementById('f-cf').value)return false;
      if(!document.getElementById('f-via').value)return false;
      if(!document.getElementById('f-cap').value)return false;
    }
  }
  return true;
}"""
html = html.replace(old_validate, new_validate)

# Aggiungi oninput ai campi step 2 per abilitare bottone dinamicamente
html = html.replace(
    'id="f-nome" type="text" placeholder="Mario"',
    'id="f-nome" type="text" placeholder="Mario" oninput="checkStep2()"'
)
html = html.replace(
    'id="f-cognome" type="text" placeholder="Rossi"',
    'id="f-cognome" type="text" placeholder="Rossi" oninput="checkStep2()"'
)
html = html.replace(
    'id="f-email" type="email" placeholder="mario@email.it"',
    'id="f-email" type="email" placeholder="mario@email.it" oninput="checkStep2()"'
)
html = html.replace(
    'id="f-tel" type="tel" placeholder="+39 333 1234567"',
    'id="f-tel" type="tel" placeholder="+39 333 1234567" oninput="checkStep2()"'
)

# selectRole chiama checkStep2
old_role = "function selectRole(r){"
new_role = "function selectRole(r){\n  setTimeout(checkStep2,50);"
html = html.replace(old_role, new_role)

# Step 2 bottone parte disabilitato
html = html.replace(
    'id="btn-avanti-2" onclick="if(validateStep(2))goTo(3)">Avanti →</button>',
    'id="btn-avanti-2" disabled onclick="if(validateStep(2))goTo(3)">Avanti →</button>'
)

with open('public/index.html', 'w') as f:
    f.write(html)

print("Patch bottoni applicata!")
print("  Step 1: Avanti disabilitato finche non selezioni corso")
print("  Step 2: Avanti disabilitato finche non compili tutti i campi")

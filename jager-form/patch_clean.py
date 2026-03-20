with open('public/index.html', 'r') as f:
    html = f.read()

# Disabilita showFarmaciaFields - non deve piu mostrare i vecchi campi dopo VIES
old = """function showFarmaciaFields(){
  var ids=['f1','f2','f3','f4','f5'];
  ids.forEach(function(id,i){
    setTimeout(function(){document.getElementById(id).classList.add('visible');},i*100);
  });
}"""
new = """function showFarmaciaFields(){
  // disabilitato - ora usiamo la card VIES
}"""
html = html.replace(old, new)

# Rimuovi anche chiamata a showFarmaciaFields da lookupPIVA quando PIVA valida senza nome
html = html.replace(
    "showFarmaciaFields();\n        el.className='field-input valid';",
    "el.className='field-input valid';"
)

# Rinomina SDI field label - rimuovi PEC
html = html.replace('Codice SDI / PEC <span class="required">*</span>', 'Codice SDI <span class="required">*</span>')
html = html.replace('ABC1234 oppure pec@farmacia.it', 'es. ABC1234')

with open('public/index.html', 'w') as f:
    f.write(html)

print("Patch pulita applicata!")

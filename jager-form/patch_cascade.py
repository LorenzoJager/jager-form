with open('public/index.html', 'r') as f:
    html = f.read()

# Nasconde i vecchi campi cascata quando VIES verifica
old_fn = "function showViesVerified(name, addr){\n  var r=document.getElementById('piva-result');\n  r.style.display='block';\n  document.getElementById('vies-ok').style.display='block';\n  document.getElementById('vies-err').style.display='none';\n  document.getElementById('vies-name-ok').textContent=name;\n  document.getElementById('vies-addr-ok').textContent=addr||'Indirizzo registrato nel VIES';\n  document.getElementById('f-ragsoc').value=name;\n  document.getElementById('f5').classList.add('visible');\n  // vecchia funzione disabilitata\n  return;\n}"

new_fn = "function showViesVerified(name, addr){\n  var r=document.getElementById('piva-result');\n  r.style.display='block';\n  document.getElementById('vies-ok').style.display='block';\n  document.getElementById('vies-err').style.display='none';\n  document.getElementById('vies-name-ok').textContent=name;\n  document.getElementById('vies-addr-ok').textContent=addr||'Indirizzo registrato nel VIES';\n  // Nascondi vecchi campi cascata - ora sono nella card\n  ['f1','f2','f3','f4','f5'].forEach(function(id){var el=document.getElementById(id);if(el)el.classList.remove('visible');});\n  document.getElementById('f-ragsoc').value=name;\n}"

html = html.replace(old_fn, new_fn)

# Quando VIES fallisce, mostra i vecchi campi per inserimento manuale
old_err_fn = "function showViesError(msg){\n  var r=document.getElementById('piva-result');\n  r.style.display='block';\n  document.getElementById('vies-ok').style.display='none';\n  document.getElementById('vies-err').style.display='block';\n  document.getElementById('vies-err-text').textContent=msg||'P.IVA non trovata su VIES';\n  return;\n}"

new_err_fn = "function showViesError(msg){\n  var r=document.getElementById('piva-result');\n  r.style.display='block';\n  document.getElementById('vies-ok').style.display='none';\n  document.getElementById('vies-err').style.display='block';\n  document.getElementById('vies-err-text').textContent=msg||'P.IVA non trovata su VIES';\n}"

html = html.replace(old_err_fn, new_err_fn)

# enableManual mostra i vecchi campi
old_manual = "function enableManual(){"
new_manual = "function enableManual(){\n  document.getElementById('piva-result').style.display='none';\n  var ids=['f1','f2','f3','f4','f5'];\n  ids.forEach(function(id,i){setTimeout(function(){var el=document.getElementById(id);if(el)el.classList.add('visible');},i*100);});"
html = html.replace(old_manual, new_manual, 1)

# Reset quando cambia la PIVA
old_reset = "document.getElementById('piva-result').className='piva-result';"
new_reset = "document.getElementById('piva-result').style.display='none';\n      if(document.getElementById('vies-ok'))document.getElementById('vies-ok').style.display='none';\n      if(document.getElementById('vies-err'))document.getElementById('vies-err').style.display='none';\n      ['f1','f2','f3','f4','f5'].forEach(function(id){var el=document.getElementById(id);if(el)el.classList.remove('visible');});"
html = html.replace(old_reset, new_reset)

with open('public/index.html', 'w') as f:
    f.write(html)

print("Patch cascade applicata!")
print("  Vecchi campi nascosti dopo verifica VIES")
print("  Card verde/arancione come unica interfaccia post-verifica")

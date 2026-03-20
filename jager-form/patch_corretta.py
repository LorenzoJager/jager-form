with open('public/index.html', 'r') as f:
    html = f.read()

# FIX 1: sostituisce piva-result div con card strutturata
old = '<div class="piva-result" id="piva-result"></div>'
new = '''<div id="piva-result" style="display:none;margin-top:10px;border-radius:12px;overflow:hidden;">
  <!-- stato verde: verificato -->
  <div id="vies-ok" style="display:none;">
    <div style="background:#0f6e56;padding:12px 16px;display:flex;align-items:center;gap:10px;">
      <div style="width:22px;height:22px;border-radius:50%;background:rgba(255,255,255,0.2);display:flex;align-items:center;justify-content:center;flex-shrink:0;">
        <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="3" stroke-linecap="round"><polyline points="20 6 9 17 4 12"/></svg>
      </div>
      <span style="font-size:15px;font-weight:700;color:#fff;">Dati confermati da VIES</span>
      <span style="font-size:10px;background:rgba(255,255,255,0.2);color:#fff;padding:2px 8px;border-radius:10px;margin-left:auto;">Verificato</span>
    </div>
    <div style="background:#e1f5ee;border:1.5px solid #0f6e56;border-top:none;padding:14px 16px;">
      <div style="display:grid;grid-template-columns:120px 1fr;gap:6px;font-size:13px;margin-bottom:4px;">
        <span style="color:#1a5e40;font-weight:500;">Ragione sociale</span>
        <span style="color:#0a4a38;font-weight:700;" id="vies-name-ok">—</span>
        <span style="color:#1a5e40;font-weight:500;">Indirizzo</span>
        <span style="color:#0a4a38;" id="vies-addr-ok">—</span>
      </div>
    </div>
    <div style="background:#fff8e6;border:2px solid #e67e22;border-top:none;padding:14px 16px;">
      <div style="display:flex;align-items:center;gap:8px;margin-bottom:14px;">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#e67e22" stroke-width="2.5" stroke-linecap="round"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg>
        <span style="font-size:14px;font-weight:700;color:#7a4a00;">Completa questi 2 campi obbligatori</span>
      </div>
      <div style="margin-bottom:14px;">
        <div style="font-size:12px;font-weight:600;color:#e67e22;margin-bottom:6px;">CAP e Citta sede legale *</div>
        <div style="display:grid;grid-template-columns:100px 1fr 58px;gap:8px;">
          <input class="field-input" id="f-cap2" type="text" placeholder="CAP" maxlength="5" oninput="lookupCAP('f-cap2','f-citta2','f-prov2')" style="border:1.5px solid #e67e22;background:#fffdf5;font-weight:500;"/>
          <input class="field-input" id="f-citta2" type="text" placeholder="Citta automatica" style="background:#fffdf5;"/>
          <input class="field-input" id="f-prov2" type="text" placeholder="PR" maxlength="2" style="background:#fffdf5;"/>
        </div>
        <div style="font-size:11px;color:#a06000;margin-top:4px;">Inserisci il CAP — citta e provincia si completano in automatico</div>
      </div>
      <div>
        <div style="font-size:12px;font-weight:600;color:#e67e22;margin-bottom:6px;">Codice SDI * <span style="font-size:10px;background:#e67e22;color:#fff;padding:2px 7px;border-radius:8px;margin-left:4px;">fatturazione elettronica</span></div>
        <input class="field-input" id="f-sdi" type="text" placeholder="es. ABC1234" style="border:1.5px solid #e67e22;background:#fffdf5;font-weight:500;"/>
        <div style="font-size:11px;color:#a06000;margin-top:4px;">Il codice SDI a 7 caratteri e obbligatorio per ricevere la fattura elettronica</div>
      </div>
    </div>
  </div>
  <!-- stato rosso: errore -->
  <div id="vies-err" style="display:none;background:#faece7;border:1.5px solid #993c1d;border-radius:10px;padding:14px 16px;">
    <div style="display:flex;align-items:center;gap:8px;margin-bottom:10px;">
      <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#993c1d" stroke-width="2.5" stroke-linecap="round"><circle cx="12" cy="12" r="10"/><line x1="15" y1="9" x2="9" y2="15"/><line x1="9" y1="9" x2="15" y2="15"/></svg>
      <span style="font-size:14px;font-weight:700;color:#7a2a1a;" id="vies-err-text">P.IVA non trovata su VIES</span>
    </div>
  </div>
</div>'''

html = html.replace(old, new)

# FIX 2: aggiorna showViesVerified per usare i nuovi ID
old_fn = 'function showViesVerified(name, addr){'
new_fn = '''function showViesVerified(name, addr){
  var r=document.getElementById('piva-result');
  r.style.display='block';
  document.getElementById('vies-ok').style.display='block';
  document.getElementById('vies-err').style.display='none';
  document.getElementById('vies-name-ok').textContent=name;
  document.getElementById('vies-addr-ok').textContent=addr||'Indirizzo registrato nel VIES';
  document.getElementById('f-ragsoc').value=name;
  document.getElementById('f5').classList.add('visible');
  // vecchia funzione disabilitata
  return;
}
function showViesVerified_OLD(name, addr){'''
html = html.replace(old_fn, new_fn)

# FIX 3: aggiorna showViesError
old_err = 'function showViesError(msg){'
new_err = '''function showViesError(msg){
  var r=document.getElementById('piva-result');
  r.style.display='block';
  document.getElementById('vies-ok').style.display='none';
  document.getElementById('vies-err').style.display='block';
  document.getElementById('vies-err-text').textContent=msg||'P.IVA non trovata su VIES';
  return;
}
function showViesError_OLD(msg){'''
html = html.replace(old_err, new_err)

# FIX 4: bottone manuale dopo 5 secondi nel loading
old_manual_timer = "var manualTimer=setTimeout(function(){var mb=document.getElementById('vies-manual-timeout-btn');if(mb)mb.style.display='block';},5000);"
if old_manual_timer not in html:
    # Aggiunge il timer nel lookupPIVA
    html = html.replace(
        "spin.style.display='block';",
        "spin.style.display='block';\n    var manualTimer=setTimeout(function(){var mb=document.getElementById('vies-manual-timeout-btn');if(mb)mb.style.display='block';},5000);"
    )

# FIX 5: spazio extra sopra i bottoni step 3
html = html.replace(
    '<div class="form-nav">\n        <button class="btn-back" onclick="goTo(2)">',
    '<div class="form-nav" style="margin-top:28px;">\n        <button class="btn-back" onclick="goTo(2)">'
)

with open('public/index.html', 'w') as f:
    f.write(html)

print("Patch applicata!")
print("  - Card VIES verde con dati confermati")
print("  - Sezione arancione CAP + SDI obbligatori")
print("  - Card rossa per errori VIES")
print("  - Spazio extra sopra bottoni step 3")

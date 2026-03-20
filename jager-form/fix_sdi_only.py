with open('public/index.html', 'r') as f:
    html = f.read()

# Sostituisce la sezione arancione con solo SDI
old_orange = '''    <div style="background:#fff8e6;border:2px solid #e67e22;border-top:none;padding:14px 16px;">
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
    </div>'''

new_orange = '''    <div style="background:#fff8e6;border:2px solid #e67e22;border-top:none;padding:14px 16px;">
      <div style="display:flex;align-items:center;gap:8px;margin-bottom:12px;">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#e67e22" stroke-width="2.5" stroke-linecap="round"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg>
        <span style="font-size:14px;font-weight:700;color:#7a4a00;">Inserisci il Codice SDI</span>
      </div>
      <div style="font-size:12px;font-weight:600;color:#e67e22;margin-bottom:6px;">
        Codice SDI * 
        <span style="font-size:10px;background:#e67e22;color:#fff;padding:2px 7px;border-radius:8px;margin-left:4px;">fatturazione elettronica</span>
      </div>
      <input class="field-input" id="f-sdi" type="text" placeholder="es. ABC1234" style="border:1.5px solid #e67e22;background:#fffdf5;font-weight:500;font-size:15px;padding:10px 12px;"/>
      <div style="font-size:11px;color:#a06000;margin-top:6px;">Il codice SDI a 7 caratteri e obbligatorio per ricevere la fattura elettronica. Lo trovi nelle impostazioni del tuo software di fatturazione.</div>
      <!-- campi nascosti per compatibilita dati -->
      <input type="hidden" id="f-cap2" value=""/>
      <input type="hidden" id="f-citta2" value=""/>
      <input type="hidden" id="f-prov2" value=""/>
    </div>'''

if old_orange in html:
    html = html.replace(old_orange, new_orange)
    print("Sezione arancione aggiornata - solo SDI")
else:
    print("ATTENZIONE: stringa non trovata esattamente")

# Aggiorna lookupPIVA per estrarre CAP/citta dall'indirizzo VIES automaticamente
old_addr = "var n=document.getElementById('vies-name-ok');if(n)n.textContent=name;\n          var a=document.getElementById('vies-addr-ok');if(a)a.textContent=addr||'Indirizzo registrato VIES';"
new_addr = """var n=document.getElementById('vies-name-ok');if(n)n.textContent=name;
          var a=document.getElementById('vies-addr-ok');if(a)a.textContent=addr||'Indirizzo registrato VIES';
          // Estrai CAP da indirizzo VIES e precompila campi nascosti
          var capMatch=addr.match(/\\b(\\d{5})\\b/);
          if(capMatch){
            var cap2=document.getElementById('f-cap2');if(cap2)cap2.value=capMatch[1];
          }"""
html = html.replace(old_addr, new_addr)

with open('public/index.html', 'w') as f:
    f.write(html)

print("Fix completato!")

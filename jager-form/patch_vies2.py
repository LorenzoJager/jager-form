with open('public/index.html', 'r') as f:
    html = f.read()

# FIX 1+2: sostituisce il box di caricamento VIES con versione grande + bottone manuale dopo 5 secondi
old_loading = '''<div id="vies-loading-text" style="display:none;margin-top:10px;padding:14px 16px;background:#e8f3fb;border:1.5px solid #0d6fa8;border-radius:10px;">
          <div style="display:flex;align-items:center;gap:10px;margin-bottom:8px;">
            <div style="width:20px;height:20px;border:3px solid #b8d8ee;border-top-color:#0d6fa8;border-radius:50%;animation:spin 0.7s linear infinite;flex-shrink:0;"></div>
            <span style="font-size:15px;font-weight:600;color:#0a4f7a;">Verifica Partita IVA in corso...</span>
          </div>
          <div style="font-size:13px;color:#1a5e8a;line-height:1.6;padding-left:30px;">
            Stiamo verificando la tua Partita IVA sul registro europeo VIES.<br>
            <strong>Attendi qualche secondo</strong> prima di proseguire.
          </div>
          <div style="margin-top:10px;padding-left:30px;">
            <div style="height:6px;background:#c8dcea;border-radius:3px;overflow:hidden;">
              <div style="height:6px;background:#0d6fa8;border-radius:3px;width:100%;animation:progress-pulse 1.5s ease-in-out infinite;"></div>
            </div>
          </div>
        </div>'''

new_loading = '''<div id="vies-loading-text" style="display:none;margin-top:12px;border-radius:12px;overflow:hidden;border:2px solid #0d6fa8;">
          <div style="background:#0d6fa8;padding:12px 16px;display:flex;align-items:center;gap:12px;">
            <div style="width:24px;height:24px;border:3px solid rgba(255,255,255,0.4);border-top-color:#fff;border-radius:50%;animation:spin2 0.7s linear infinite;flex-shrink:0;"></div>
            <span style="font-size:16px;font-weight:700;color:#fff;">Verifica Partita IVA in corso...</span>
          </div>
          <div style="background:#e8f3fb;padding:14px 16px;">
            <div style="font-size:14px;color:#0a4f7a;line-height:1.7;margin-bottom:12px;">
              Stiamo controllando la tua Partita IVA sul <strong>registro europeo VIES</strong>.<br>
              ⏳ <strong>Attendi qualche secondo</strong> prima di proseguire.
            </div>
            <div style="height:8px;background:#c8dcea;border-radius:4px;overflow:hidden;">
              <div style="height:8px;background:#0d6fa8;border-radius:4px;animation:progress-slide 1.8s ease-in-out infinite;"></div>
            </div>
            <div id="vies-manual-timeout-btn" style="display:none;margin-top:14px;text-align:center;">
              <div style="font-size:13px;color:#666;margin-bottom:8px;">La verifica sta richiedendo più tempo del solito.</div>
              <button onclick="enableFullManual()" style="background:#fff;border:1.5px solid #0d6fa8;color:#0d6fa8;padding:10px 20px;border-radius:8px;font-size:14px;font-weight:500;cursor:pointer;font-family:inherit;">
                Inserisci i dati manualmente →
              </button>
            </div>
          </div>
        </div>'''

html = html.replace(old_loading, new_loading)

# Aggiorna animazione spin per il nuovo spinner bianco
html = html.replace(
    '@keyframes spin{to{transform:translateY(-50%) rotate(360deg);}}',
    '@keyframes spin{to{transform:translateY(-50%) rotate(360deg);}}\n@keyframes spin2{to{transform:rotate(360deg);}}\n@keyframes progress-slide{0%{width:0%;margin-left:0}70%{width:80%;margin-left:0}100%{width:80%;margin-left:100%}}'
)

# FIX 2: timer 5 secondi per mostrare bottone manuale
old_show_loading = "var lt=document.getElementById('vies-loading-text');if(lt){lt.style.display='flex';}"
new_show_loading = """var lt=document.getElementById('vies-loading-text');if(lt){lt.style.display='block';}
    var manualTimer=setTimeout(function(){var mb=document.getElementById('vies-manual-timeout-btn');if(mb)mb.style.display='block';},5000);"""
html = html.replace(old_show_loading, new_show_loading)

old_hide_loading = "var lt=document.getElementById('vies-loading-text');if(lt){lt.style.display='none';}"
new_hide_loading = """var lt=document.getElementById('vies-loading-text');if(lt){lt.style.display='none';}
      if(typeof manualTimer!=='undefined')clearTimeout(manualTimer);
      var mb=document.getElementById('vies-manual-timeout-btn');if(mb)mb.style.display='none';"""
html = html.replace(old_hide_loading, new_hide_loading)

# FIX 3: ridisegna la vies-card verified con info confermate in cima + campi richiesti evidenziati
old_verified_card = '''          <!-- verified state -->
          <div class="vies-card-verified" id="vies-verified" style="display:none;">
            <div class="vies-verified-row">
              <div class="vies-check-icon">
                <svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="3" stroke-linecap="round"><polyline points="20 6 9 17 4 12"/></svg>
              </div>
              <span class="vies-company-name" id="vies-name">—</span>
              <span class="vies-piva-badge">VIES verificata</span>
            </div>
            <div class="vies-address-row">
              <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="#0f6e56" stroke-width="2" stroke-linecap="round"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/></svg>
              <span class="vies-address-text" id="vies-addr">—</span>
            </div>
            <div class="vies-divider"></div>
            <div class="vies-manual-section">
              <div class="vies-manual-title">
                <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="#e67e22" stroke-width="2.5" stroke-linecap="round"><path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"/><path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"/></svg>
                Completa manualmente
              </div>
              <div style="display:grid;grid-template-columns:88px 1fr 60px;gap:10px;margin-bottom:10px;">
                <div>
                  <div class="field-label highlight-label">CAP <span class="required">*</span></div>
                  <input class="field-input highlight" id="f-cap2" type="text" placeholder="50100" maxlength="5" oninput="lookupCAP(\'f-cap2\',\'f-citta2\',\'f-prov2\')"/>
                </div>
                <div>
                  <div class="field-label">Città <span class="required">*</span></div>
                  <input class="field-input" id="f-citta2" type="text" placeholder="Firenze"/>
                </div>
                <div>
                  <div class="field-label">Prov.</div>
                  <input class="field-input" id="f-prov2" type="text" placeholder="FI" maxlength="2"/>
                </div>
              </div>
              <div>
                <div class="field-label highlight-label">Codice SDI / PEC <span class="required">*</span><span class="tag">e-fattura</span></div>
                <input class="field-input highlight" id="f-sdi" type="text" placeholder="ABC1234 oppure pec@farmacia.it"/>
                <div class="highlight-hint">
                  <svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="#e67e22" stroke-width="2.5"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg>
                  Richiesto per la fatturazione elettronica B2B
                </div>
              </div>
            </div>
          </div>'''

new_verified_card = '''          <!-- verified state -->
          <div class="vies-card-verified" id="vies-verified" style="display:none;">
            <!-- SEZIONE VERDE: dati confermati da VIES -->
            <div style="background:#e1f5ee;border:1.5px solid #0f6e56;border-radius:10px;padding:14px 16px;margin-bottom:14px;">
              <div style="display:flex;align-items:center;gap:8px;margin-bottom:10px;">
                <div style="width:22px;height:22px;border-radius:50%;background:#0f6e56;display:flex;align-items:center;justify-content:center;flex-shrink:0;">
                  <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="3" stroke-linecap="round"><polyline points="20 6 9 17 4 12"/></svg>
                </div>
                <span style="font-size:13px;font-weight:700;color:#0a4a38;">Dati confermati da VIES</span>
                <span style="font-size:10px;background:#0f6e56;color:#fff;padding:2px 8px;border-radius:10px;margin-left:auto;">Verificato</span>
              </div>
              <div style="display:grid;grid-template-columns:110px 1fr;gap:6px;font-size:13px;">
                <span style="color:#1a5e40;font-weight:500;">Ragione sociale</span>
                <span style="color:#0a4a38;font-weight:700;" id="vies-name">—</span>
                <span style="color:#1a5e40;font-weight:500;">Indirizzo</span>
                <span style="color:#0a4a38;" id="vies-addr">—</span>
              </div>
            </div>
            <!-- SEZIONE ARANCIONE: campi da completare -->
            <div style="background:#fff8e6;border:2px solid #e67e22;border-radius:10px;padding:14px 16px;">
              <div style="display:flex;align-items:center;gap:8px;margin-bottom:12px;">
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#e67e22" stroke-width="2.5" stroke-linecap="round"><path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"/><path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"/></svg>
                <span style="font-size:14px;font-weight:700;color:#7a4a00;">Completa questi 2 campi obbligatori</span>
              </div>
              <!-- CAP + Città inline -->
              <div style="margin-bottom:12px;">
                <div style="font-size:12px;font-weight:600;color:#e67e22;margin-bottom:5px;">📍 CAP e Città sede legale *</div>
                <div style="display:grid;grid-template-columns:100px 1fr 58px;gap:8px;">
                  <input class="field-input" id="f-cap2" type="text" placeholder="CAP" maxlength="5" oninput="lookupCAP(\'f-cap2\',\'f-citta2\',\'f-prov2\')" style="border:1.5px solid #e67e22;background:#fffdf5;font-weight:500;"/>
                  <input class="field-input" id="f-citta2" type="text" placeholder="Città (automatica)" style="background:#fffdf5;"/>
                  <input class="field-input" id="f-prov2" type="text" placeholder="PR" maxlength="2" style="background:#fffdf5;"/>
                </div>
                <div style="font-size:11px;color:#a06000;margin-top:4px;">Inserisci il CAP — città e provincia si completano in automatico</div>
              </div>
              <!-- Codice SDI -->
              <div>
                <div style="font-size:12px;font-weight:600;color:#e67e22;margin-bottom:5px;">🧾 Codice SDI *<span style="font-size:10px;background:#e67e22;color:#fff;padding:2px 7px;border-radius:8px;margin-left:6px;font-weight:500;">fatturazione elettronica</span></div>
                <input class="field-input" id="f-sdi" type="text" placeholder="es. ABC1234" style="border:1.5px solid #e67e22;background:#fffdf5;font-weight:500;"/>
                <div style="font-size:11px;color:#a06000;margin-top:4px;">Il codice SDI a 7 caratteri è obbligatorio per ricevere la fattura elettronica</div>
              </div>
            </div>
          </div>'''

html = html.replace(old_verified_card, new_verified_card)

with open('public/index.html', 'w') as f:
    f.write(html)

print("Patch applicata!")
print("  Fix 1: box VIES loading grande e visibile")
print("  Fix 2: bottone manuale dopo 5 secondi")
print("  Fix 3: card VIES verde + sezione arancione campi obbligatori")

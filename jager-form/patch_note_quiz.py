with open('public/index.html', 'r') as f:
    html = f.read()

# FIX 1: Rimuovi "Altre note o richieste particolari"
old_note = '''      <div class="field-single">
        <div class="field-label">Altre note o richieste particolari</div>
        <textarea class="field-input" id="f-note" rows="2" placeholder="Eventuali esigenze logistiche o domande..."></textarea>
      </div>'''
html = html.replace(old_note, '')
print("1. Campo note rimosso")

# FIX 2a: Aggiungi bottone "Segna tutti NO" e SI/NO più visibili
old_header = '''          <div style="display:grid;grid-template-columns:1fr auto;align-items:center;padding:4px 0 6px;border-bottom:0.5px solid #f0d070;margin-bottom:4px;">
            <span style="font-size:11px;font-weight:600;color:#9a7a1a;"></span>
            <div style="display:flex;gap:24px;padding-right:8px;">
              <span style="font-size:11px;font-weight:700;color:#9a7a1a;width:28px;text-align:center;">SI</span>
              <span style="font-size:11px;font-weight:700;color:#9a7a1a;width:28px;text-align:center;">NO</span>
            </div>
          </div>'''

new_header = '''          <div style="display:grid;grid-template-columns:1fr auto;align-items:center;padding:6px 0 8px;border-bottom:1.5px solid #e8c840;margin-bottom:6px;">
            <button onclick="segnaNoTutti()" type="button" style="background:#fff8e1;border:1px solid #e8c840;color:#7a5c00;padding:5px 12px;border-radius:20px;font-size:12px;font-weight:600;cursor:pointer;font-family:inherit;">Segna tutti NO</button>
            <div style="display:flex;gap:24px;padding-right:8px;">
              <span style="font-size:14px;font-weight:800;color:#2a7a00;width:28px;text-align:center;">SI</span>
              <span style="font-size:14px;font-weight:800;color:#c0392b;width:28px;text-align:center;">NO</span>
            </div>
          </div>'''

if old_header in html:
    html = html.replace(old_header, new_header)
    print("2. Header SI/NO aggiornato con bottone Segna tutti NO")
else:
    print("ATTENZIONE: header non trovato")

# FIX 2b: Aggiungi funzione segnaNoTutti
segna_fn = """
function segnaNoTutti(){
  ['vegetariano','vegano','lattosio','celiaco'].forEach(function(n){
    var radio=document.querySelector('input[name="all-'+n+'"][value="no"]');
    if(radio){radio.checked=true;}
  });
  checkAllergie();
}
"""
html = html.replace('</script>\n</body>', segna_fn + '</script>\n</body>')
print("3. Funzione segnaNoTutti aggiunta")

# FIX 3: Badge quiz più grandi
old_badges = '''          <div class="quiz-badge-row">
            <span class="quiz-badge opt"><svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="#0a4f7a" stroke-width="2.5"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg>Facoltativo</span>
            <span class="quiz-badge anon"><svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="#0a4a38" stroke-width="2.5"><rect x="3" y="11" width="18" height="11" rx="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/></svg>Risposte anonime</span>
            <span class="quiz-badge util"><svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="#7a5c00" stroke-width="2.5"><polyline points="22 12 18 12 15 21 9 3 6 12 2 12"/></svg>Migliora il corso</span>
          </div>'''

new_badges = '''          <div style="display:flex;gap:10px;justify-content:center;flex-wrap:wrap;margin-bottom:16px;">
            <span style="display:inline-flex;align-items:center;gap:7px;font-size:14px;font-weight:700;padding:10px 18px;border-radius:30px;background:#e8f3fb;color:#0a4f7a;border:2px solid #0d6fa8;">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#0a4f7a" stroke-width="2.5"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg>
              FACOLTATIVO
            </span>
            <span style="display:inline-flex;align-items:center;gap:7px;font-size:14px;font-weight:700;padding:10px 18px;border-radius:30px;background:#e1f5ee;color:#0a4a38;border:2px solid #0f6e56;">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#0a4a38" stroke-width="2.5"><rect x="3" y="11" width="18" height="11" rx="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/></svg>
              ANONIMO
            </span>
            <span style="display:inline-flex;align-items:center;gap:7px;font-size:14px;font-weight:700;padding:10px 18px;border-radius:30px;background:#fff8e1;color:#7a5c00;border:2px solid #e8c840;">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#7a5c00" stroke-width="2.5"><polyline points="22 12 18 12 15 21 9 3 6 12 2 12"/></svg>
              MIGLIORA IL CORSO
            </span>
          </div>'''

if old_badges in html:
    html = html.replace(old_badges, new_badges)
    print("4. Badge quiz aggiornati")
else:
    print("Badge non trovati - potrebbero essere gia aggiornati")

with open('public/index.html', 'w') as f:
    f.write(html)

print("Patch completata!")

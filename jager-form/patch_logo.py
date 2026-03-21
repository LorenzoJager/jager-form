import base64
import os

with open('public/index.html', 'r') as f:
    html = f.read()

# FIX 1: numero telefono formato corretto
html = html.replace('tel:+393406219415', 'tel:+393406219415')
html = html.replace('340 621 9415', '+39 340 621 9415')
print("1. Telefono aggiornato")

# FIX 2: carica logo come base64
logo_path = '/mnt/user-data/uploads/jager_logo_original_exact.png'
if os.path.exists(logo_path):
    with open(logo_path, 'rb') as f:
        logo_b64 = base64.b64encode(f.read()).decode('utf-8')
    logo_src = f'data:image/png;base64,{logo_b64}'
    print("2. Logo caricato come base64")
else:
    logo_src = ''
    print("ATTENZIONE: logo non trovato")

# FIX 3: sostituisce logo SVG con immagine reale + nuovo testo
old_nav = '''  <div class="nav-logo">
    <div class="nav-logo-icon">
      <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 2L2 7l10 5 10-5-10-5z"/><path d="M2 17l10 5 10-5"/><path d="M2 12l10 5 10-5"/></svg>
    </div>
    <div>
      <div class="nav-name">JAGER GALENICA</div>
      <div class="nav-sub">Scuola di Galenica · Cortona</div>
    </div>
  </div>'''

new_nav = f'''  <div class="nav-logo">
    <img src="{logo_src}" alt="Jager Galenica" style="width:44px;height:44px;border-radius:50%;object-fit:cover;flex-shrink:0;"/>
    <div>
      <div class="nav-name">JÄGER GALENICA</div>
      <div class="nav-sub">Scuola Galenica del Dr. Peter Jäger</div>
    </div>
  </div>'''

if old_nav in html:
    html = html.replace(old_nav, new_nav)
    print("3. Logo e titolo aggiornati")
else:
    print("ATTENZIONE: nav logo non trovato")

with open('public/index.html', 'w') as f:
    f.write(html)

print("Patch logo completata!")

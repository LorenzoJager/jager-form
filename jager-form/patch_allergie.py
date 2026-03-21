with open('public/index.html', 'r') as f:
    html = f.read()

# Trova e sostituisce tutta la griglia allergie con versione SI/NO obbligatoria
old_grid = '''        <div style="display:grid;grid-template-columns:1fr 1fr;gap:8px;margin-top:10px;margin-bottom:10px;">
          <label style="display:flex;align-items:center;gap:8px;padding:8px 10px;background:#fff;border-radius:8px;border:0.5px solid #f0d070;cursor:pointer;font-size:13px;color:#5a4000;">
            <input type="checkbox" id="all-vegetariano" style="width:16px;height:16px;cursor:pointer;accent-color:#0d6fa8;"> Vegetariano
          </label>
          <label style="display:flex;align-items:center;gap:8px;padding:8px 10px;background:#fff;border-radius:8px;border:0.5px solid #f0d070;cursor:pointer;font-size:13px;color:#5a4000;">
            <input type="checkbox" id="all-vegano" style="width:16px;height:16px;cursor:pointer;accent-color:#0d6fa8;"> Vegano
          </label>
          <label style="display:flex;align-items:center;gap:8px;padding:8px 10px;background:#fff;border-radius:8px;border:0.5px solid #f0d070;cursor:pointer;font-size:13px;color:#5a4000;">
            <input type="checkbox" id="all-lattosio" style="width:16px;height:16px;cursor:pointer;accent-color:#0d6fa8;"> Intolleranza al lattosio
          </label>
          <label style="display:flex;align-items:center;gap:8px;padding:8px 10px;background:#fff;border-radius:8px;border:0.5px solid #f0d070;cursor:pointer;font-size:13px;color:#5a4000;">
            <input type="checkbox" id="all-celiaco" style="width:16px;height:16px;cursor:pointer;accent-color:#0d6fa8;"> Celiachia / Glutine
          </label>
          <label style="display:flex;align-items:center;gap:8px;padding:8px 10px;background:#fff;border-radius:8px;border:0.5px solid #f0d070;cursor:pointer;font-size:13px;color:#5a4000;">
            <input type="checkbox" id="all-fruttasecca" style="width:16px;height:16px;cursor:pointer;accent-color:#0d6fa8;"> Allergia frutta a guscio
          </label>
          <label style="display:flex;align-items:center;gap:8px;padding:8px 10px;background:#fff;border-radius:8px;border:0.5px solid #f0d070;cursor:pointer;font-size:13px;color:#5a4000;">
            <input type="checkbox" id="all-uova" style="width:16px;height:16px;cursor:pointer;accent-color:#0d6fa8;"> Allergia alle uova
          </label>
          <label style="display:flex;align-items:center;gap:8px;padding:8px 10px;background:#fff;border-radius:8px;border:0.5px solid #f0d070;cursor:pointer;font-size:13px;color:#5a4000;">
            <input type="checkbox" id="all-pesce" style="width:16px;height:16px;cursor:pointer;accent-color:#0d6fa8;"> Allergia al pesce / molluschi
          </label>
          <label style="display:flex;align-items:center;gap:8px;padding:8px 10px;background:#fff;border-radius:8px;border:0.5px solid #f0d070;cursor:pointer;font-size:13px;color:#5a4000;">
            <input type="checkbox" id="all-halal" style="width:16px;height:16px;cursor:pointer;accent-color:#0d6fa8;"> Dieta Halal / Kosher
          </label>
        </div>'''

new_grid = '''        <div style="margin-top:10px;margin-bottom:10px;">
          <div style="display:grid;grid-template-columns:1fr auto;align-items:center;padding:4px 0 6px;border-bottom:0.5px solid #f0d070;margin-bottom:4px;">
            <span style="font-size:11px;font-weight:600;color:#9a7a1a;"></span>
            <div style="display:flex;gap:24px;padding-right:8px;">
              <span style="font-size:11px;font-weight:700;color:#9a7a1a;width:28px;text-align:center;">SI</span>
              <span style="font-size:11px;font-weight:700;color:#9a7a1a;width:28px;text-align:center;">NO</span>
            </div>
          </div>
          <div id="all-row-vegetariano" class="all-row" style="display:grid;grid-template-columns:1fr auto;align-items:center;padding:9px 0;border-bottom:0.5px solid #f9f0c8;">
            <span style="font-size:13px;color:#5a4000;">Vegetariano</span>
            <div style="display:flex;gap:24px;padding-right:8px;">
              <input type="radio" name="all-vegetariano" value="si" style="width:18px;height:18px;cursor:pointer;accent-color:#0d6fa8;" onchange="checkAllergie()">
              <input type="radio" name="all-vegetariano" value="no" style="width:18px;height:18px;cursor:pointer;accent-color:#0d6fa8;" onchange="checkAllergie()">
            </div>
          </div>
          <div id="all-row-vegano" class="all-row" style="display:grid;grid-template-columns:1fr auto;align-items:center;padding:9px 0;border-bottom:0.5px solid #f9f0c8;">
            <span style="font-size:13px;color:#5a4000;">Vegano</span>
            <div style="display:flex;gap:24px;padding-right:8px;">
              <input type="radio" name="all-vegano" value="si" style="width:18px;height:18px;cursor:pointer;accent-color:#0d6fa8;" onchange="checkAllergie()">
              <input type="radio" name="all-vegano" value="no" style="width:18px;height:18px;cursor:pointer;accent-color:#0d6fa8;" onchange="checkAllergie()">
            </div>
          </div>
          <div id="all-row-lattosio" class="all-row" style="display:grid;grid-template-columns:1fr auto;align-items:center;padding:9px 0;border-bottom:0.5px solid #f9f0c8;">
            <span style="font-size:13px;color:#5a4000;">Intolleranza al lattosio</span>
            <div style="display:flex;gap:24px;padding-right:8px;">
              <input type="radio" name="all-lattosio" value="si" style="width:18px;height:18px;cursor:pointer;accent-color:#0d6fa8;" onchange="checkAllergie()">
              <input type="radio" name="all-lattosio" value="no" style="width:18px;height:18px;cursor:pointer;accent-color:#0d6fa8;" onchange="checkAllergie()">
            </div>
          </div>
          <div id="all-row-celiaco" class="all-row" style="display:grid;grid-template-columns:1fr auto;align-items:center;padding:9px 0;">
            <span style="font-size:13px;color:#5a4000;">Celiachia / Glutine</span>
            <div style="display:flex;gap:24px;padding-right:8px;">
              <input type="radio" name="all-celiaco" value="si" style="width:18px;height:18px;cursor:pointer;accent-color:#0d6fa8;" onchange="checkAllergie()">
              <input type="radio" name="all-celiaco" value="no" style="width:18px;height:18px;cursor:pointer;accent-color:#0d6fa8;" onchange="checkAllergie()">
            </div>
          </div>
        </div>'''

if old_grid in html:
    html = html.replace(old_grid, new_grid)
    print("Griglia allergie aggiornata con SI/NO")
else:
    print("ATTENZIONE: griglia non trovata")

# Aggiunge stile disabled al btn-avanti-4 e funzione checkAllergie
old_nav_4 = '''      <div class="form-nav">
        <button class="btn-back" onclick="goTo(3)">← Indietro</button>
        <button class="btn-next" onclick="goTo(5)">Avanti →</button>
      </div>'''

new_nav_4 = '''      <div class="form-nav">
        <button class="btn-back" onclick="goTo(3)">← Indietro</button>
        <button class="btn-next" id="btn-avanti-4" disabled onclick="goTo(window.skipQuiz?6:5)">Avanti →</button>
      </div>'''

html = html.replace(old_nav_4, new_nav_4)

# Aggiunge funzione checkAllergie prima di </script>
check_fn = """
function checkAllergie(){
  var names=['vegetariano','vegano','lattosio','celiaco'];
  var allDone=names.every(function(n){
    return document.querySelector('input[name="all-'+n+'"]:checked');
  });
  var btn=document.getElementById('btn-avanti-4');
  if(btn)btn.disabled=!allDone;
}
"""
html = html.replace('</script>\n</body>', check_fn + '</script>\n</body>')

with open('public/index.html', 'w') as f:
    f.write(html)

print("Patch allergie SI/NO completata!")
print("  - Solo 4 domande: Vegetariano, Vegano, Lattosio, Celiaco")
print("  - Radio button SI/NO obbligatori")
print("  - Avanti bloccato finche non rispondi a tutte e 4")

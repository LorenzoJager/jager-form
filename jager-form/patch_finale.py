with open('public/index.html', 'r') as f:
    html = f.read()

# Estrai la sezione VIES per capire la struttura attuale
start = html.find('vies-card')
if start > 0:
    print("=== SEZIONE VIES TROVATA ===")
    print(html[start-100:start+500])
else:
    print("vies-card non trovato")

start2 = html.find('vies-loading-text')
print("\n=== LOADING TEXT ===")
print(html[start2-50:start2+300])

with open('public/index.html', 'r') as f:
    html = f.read()

# Verifica cosa c'e' nel file
if 'vies-card-verified' in html:
    print("Trovato vies-card-verified")
else:
    print("NON trovato vies-card-verified")

if 'vies-loading-text' in html:
    print("Trovato vies-loading-text")
else:
    print("NON trovato vies-loading-text")

if 'form-nav' in html:
    print("Trovato form-nav")
else:
    print("NON trovato form-nav")

# Conta quante volte appaiono
print(f"vies-card-verified appare {html.count('vies-card-verified')} volte")
print(f"vies-loading-text appare {html.count('vies-loading-text')} volte")
print(f"form-nav appare {html.count('form-nav')} volte")

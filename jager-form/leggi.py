with open('public/index.html', 'r') as f:
    html = f.read()

# Leggi la sezione attorno a piva-result
idx = html.find('piva-result')
print("=== PIVA RESULT AREA ===")
print(html[idx-50:idx+800])
print("\n=== FINE ===")

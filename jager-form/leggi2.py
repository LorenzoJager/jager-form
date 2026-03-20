with open('public/index.html', 'r') as f:
    html = f.read()

# Leggi tutto il blocco PIVA - dal campo input fino dopo il bottone manuale
start = html.find('<div class="piva-wrap">')
end = html.find('</div>', html.find('manual-btn')) + 6
print(html[start:end+200])

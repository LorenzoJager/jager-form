with open('public/index.html', 'r') as f:
    html = f.read()

old = '''<div id="vies-loading-text" style="display:none;font-size:11px;color:#0d6fa8;margin-top:6px;display:none;align-items:center;gap:6px;">
          <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="#0d6fa8" stroke-width="2.5" stroke-linecap="round"><path d="M21 12a9 9 0 1 1-6.219-8.56"/></svg>
          Verifica P.IVA in corso sul registro VIES europeo...
        </div>'''

new = '''<div id="vies-loading-text" style="display:none;margin-top:10px;padding:14px 16px;background:#e8f3fb;border:1.5px solid #0d6fa8;border-radius:10px;">
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

html = html.replace(old, new)

# Aggiungi animazione progress-pulse al CSS
old_spin = '@keyframes spin{to{transform:translateY(-50%) rotate(360deg);}}'
new_spin = '''@keyframes spin{to{transform:translateY(-50%) rotate(360deg);}}
@keyframes progress-pulse{0%{opacity:1;transform:scaleX(1)}50%{opacity:0.6;transform:scaleX(0.7)}100%{opacity:1;transform:scaleX(1)}}'''

html = html.replace(old_spin, new_spin)

with open('public/index.html', 'w') as f:
    f.write(html)

print("✅ Patch VIES loading applicata!")

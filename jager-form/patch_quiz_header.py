with open('public/index.html', 'r') as f:
    html = f.read()

old_quiz_title = '''          <div style="font-size:15px;font-weight:600;margin-bottom:10px;">Quiz di autovalutazione</div>'''

new_quiz_title = '''          <div style="font-size:15px;font-weight:600;margin-bottom:12px;">Quiz di autovalutazione</div>
          <div style="background:#fff3cd;border:2px solid #e8c840;border-radius:12px;padding:14px 16px;margin-bottom:14px;text-align:center;">
            <div style="font-size:20px;font-weight:800;color:#7a4a00;margin-bottom:4px;">QUESTO QUIZ E FACOLTATIVO</div>
            <div style="font-size:13px;color:#9a6a00;line-height:1.5;">Puoi saltarlo e cliccare direttamente su <strong>Rivedi e invia</strong> qui sotto.<br>Se scegli di rispondere, le tue risposte sono completamente anonime.</div>
          </div>'''

if old_quiz_title in html:
    html = html.replace(old_quiz_title, new_quiz_title)
    print("Header quiz aggiornato")
else:
    print("ATTENZIONE: stringa non trovata")

with open('public/index.html', 'w') as f:
    f.write(html)
print("Patch completata!")

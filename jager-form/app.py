from flask import Flask, send_from_directory, jsonify, request
import requests
import os

app = Flask(__name__, static_folder='public')

AIRTABLE_TOKEN = os.environ.get("AIRTABLE_TOKEN", "")
BREVO_API_KEY = os.environ.get("BREVO_API_KEY", "")
BASE_ID = "appJP5D3dhgHRoSsV"
TABLE_ID = "tblhYPbw4wCwSzDT3"

@app.route('/')
def index():
    return send_from_directory('public', 'index.html')

@app.route('/api/vies/<piva>')
def vies(piva):
    piva = ''.join(c for c in piva if c.isdigit())
    if len(piva) != 11:
        return jsonify({'isValid': False, 'error': 'Lunghezza P.IVA non valida'})
    try:
        url = f'https://ec.europa.eu/taxation_customs/vies/rest-api/ms/IT/vat/{piva}'
        r = requests.get(url, timeout=8)
        return jsonify(r.json())
    except Exception as e:
        return jsonify({'isValid': False, 'error': 'VIES non raggiungibile'}), 503

@app.route('/api/cap/<cap>')
def cap_lookup(cap):
    cap = ''.join(c for c in cap if c.isdigit())
    try:
        r = requests.get(f'https://api.zippopotam.us/it/{cap}', timeout=5)
        if r.ok:
            return jsonify(r.json())
        return jsonify({})
    except Exception:
        return jsonify({})

@app.route('/submit', methods=['POST'])
def submit():
    data = request.get_json()
    # Se farmacia e ragione sociale vuota, prova a recuperarla da VIES
    ragione_sociale = data.get("ragione_sociale", "")
    indirizzo = data.get("indirizzo", "")
    if data.get("tipo_fatturazione") == "farmacia":
        piva = data.get("piva", "")
        if piva:
            try:
                vies_r = requests.get(f"https://ec.europa.eu/taxation_customs/vies/rest-api/ms/IT/vat/{piva}", timeout=8)
                vies_data = vies_r.json()
                if vies_data.get("isValid") and vies_data.get("name") and vies_data["name"] != "---":
                    ragione_sociale = vies_data["name"].strip()
                if vies_data.get("address"):
                    raw = vies_data["address"].replace("\n", " ").strip()
                    import re
                    cap_match = re.search(r'\b(\d{5})\b', raw)
                    if cap_match:
                        cap_val = cap_match.group(1)
                        data["cap"] = cap_val
                        after_cap = raw[cap_match.end():].strip().rstrip(',').strip()
                        parts = after_cap.split()
                        if len(parts) >= 2:
                            data["provincia"] = parts[-1]
                            data["citta"] = ' '.join(parts[:-1])
                        elif len(parts) == 1:
                            data["citta"] = parts[0]
                        before_cap = raw[:cap_match.start()].strip().rstrip(',').strip()
                        # Separa via e numero civico
                        via_match = re.match(r'^(.*?)\s+(\d+\S*)\s*$', before_cap)
                        if via_match:
                            data["indirizzo_via"] = via_match.group(1).strip()
                            data["numero_civico"] = via_match.group(2).strip()
                        else:
                            data["indirizzo_via"] = before_cap
                            data["numero_civico"] = ""
                        if not indirizzo:
                            indirizzo = data["indirizzo_via"]
                    elif not indirizzo:
                        indirizzo = raw
            except:
                pass

    fields = {
        "Corso": data.get("corso", ""),
        "Nome": data.get("nome", ""),
        "Cognome": data.get("cognome", ""),
        "Email": data.get("email", ""),
        "Telefono": data.get("telefono", ""),
        "Ruolo": data.get("ruolo", ""),
        "Tipo Fatturazione": data.get("tipo_fatturazione", ""),
        "CF": data.get("cf", ""),
        "P_IVA": data.get("piva", ""),
        "Ragione Sociale": ragione_sociale,
        "Indirizzo": data.get("indirizzo_via", indirizzo),
        "Numero Civico": data.get("numero_civico", ""),
        "CAP": data.get("cap", ""),
        "Comune": data.get("citta", ""),
        "Provincia": data.get("provincia", ""),
        "SDI": data.get("sdi", ""),
        "Preferenze Alimentari": data.get("preferenze_alimentari", ""),
        "Note Allergie": data.get("note_allergie", ""),
        "Quiz Risposte": data.get("quiz_risposte", ""),
        "Stato": "In attesa"
    }
    partecipanti = data.get("partecipanti", [])
    if not partecipanti:
        partecipanti = [{"nome": data.get("nome",""), "cognome": data.get("cognome",""), "email": data.get("email",""), "telefono": data.get("telefono","")}]

    try:
        headers = {"Authorization": f"Bearer {AIRTABLE_TOKEN}", "Content-Type": "application/json"}
        for p in partecipanti:
            record = dict(fields)
            record["Nome"] = p.get("nome", "")
            record["Cognome"] = p.get("cognome", "")
            record["Email"] = p.get("email", "")
            record["Telefono"] = p.get("telefono", "")
            r = requests.post(
                f"https://api.airtable.com/v0/{BASE_ID}/{TABLE_ID}",
                headers=headers,
                json={"fields": record},
                timeout=10
            )
            if not r.ok:
                return jsonify({"success": False, "error": r.text}), 500
        try:
            data["partecipanti_list"] = partecipanti
            send_confirmation_email(data)
        except Exception as mail_err:
            print(f"Errore email: {mail_err}")
        return jsonify({"success": True})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

def send_confirmation_email(data):
    nome = data.get("nome", "") + " " + data.get("cognome", "")
    corso = data.get("corso", "")
    email_partecipante = data.get("email", "")
    tipo_fatt = data.get("tipo_fatturazione", "")
    telefono = data.get("telefono", "")
    ruolo = data.get("ruolo", "")

    prefs = data.get("preferenze_alimentari", [])
    note_allergie = data.get("note_allergie", "")
    allergie_parts = []
    if isinstance(prefs, list) and prefs:
        allergie_parts.extend(prefs)
    if note_allergie:
        allergie_parts.append(note_allergie)
    allergie_str = ", ".join(allergie_parts) if allergie_parts else "Nessuna"

    partecipanti_list = data.get("partecipanti_list", [])
    if not partecipanti_list:
        partecipanti_list = [{"nome": data.get("nome",""), "cognome": data.get("cognome",""), "email": data.get("email",""), "telefono": data.get("telefono","")}]
    parti_rows = ""
    for i, p in enumerate(partecipanti_list):
        p_nome = f"{p.get('nome','')} {p.get('cognome','')}".strip()
        p_email = p.get("email","")
        p_tel = p.get("telefono","")
        label = f"Partecipante {i+1}" if len(partecipanti_list) > 1 else "Partecipante"
        sep = "border-top:1px solid #e8e8e8;" if i > 0 else ""
        parti_rows += f'''<tr style="{sep}"><td style="padding:6px 0 2px;color:#666;width:40%;font-weight:600;">{label}</td><td style="padding:6px 0 2px;font-weight:500;">{p_nome}</td></tr>
        <tr><td style="padding:2px 0;color:#666;">Email</td><td style="padding:2px 0;color:#6399e7;">{p_email}</td></tr>
        <tr><td style="padding:2px 0 6px;color:#666;">Telefono</td><td style="padding:2px 0 6px;font-weight:500;">{p_tel}</td></tr>'''
    partecipanti_html = f'<table style="width:100%;font-size:13px;border-collapse:collapse;margin-top:10px;border-top:1px solid #e0e0e0;padding-top:10px;">{parti_rows}</table>'

    try:
        num_partecipanti = int(data.get("num_partecipanti", 1))
    except:
        num_partecipanti = 1
    try:
        num_accompagnatori = int(data.get("accompagnatori", 0))
    except:
        num_accompagnatori = 0
    accompagnatori_nomi = data.get("accompagnatori_nomi", [])
    if accompagnatori_nomi:
        accomp_str = ", ".join(accompagnatori_nomi)
    else:
        accomp_str = "—"

    accomp_nomi_str = (" — " + accomp_str) if accompagnatori_nomi else ""
    if tipo_fatt == "farmacia":
        fatt_rows = f"""
            <tr><td style="padding:3px 0;color:#666;width:40%;">Farmacia/Azienda</td><td style="padding:3px 0;font-weight:500;">{data.get('ragione_sociale','')}</td></tr>
            <tr><td style="padding:3px 0;color:#666;">P.IVA</td><td style="padding:3px 0;font-weight:500;">{data.get('piva','')}</td></tr>
            <tr><td style="padding:3px 0;color:#666;">SDI</td><td style="padding:3px 0;font-weight:500;">{data.get('sdi','')}</td></tr>
            <tr><td style="padding:3px 0;color:#666;">Partecipanti</td><td style="padding:3px 0;font-weight:500;">{num_partecipanti}</td></tr>
            <tr><td style="padding:3px 0;color:#666;">Accompagnatori</td><td style="padding:3px 0;font-weight:500;">{num_accompagnatori}{accomp_nomi_str}</td></tr>"""
    else:
        fatt_rows = f"""
            <tr><td style="padding:3px 0;color:#666;width:40%;">Tipo</td><td style="padding:3px 0;font-weight:500;">Privato</td></tr>
            <tr><td style="padding:3px 0;color:#666;">Codice Fiscale</td><td style="padding:3px 0;font-weight:500;">{data.get('cf','')}</td></tr>
            <tr><td style="padding:3px 0;color:#666;">Indirizzo</td><td style="padding:3px 0;font-weight:500;">{data.get('indirizzo','')} {data.get('cap','')} {data.get('citta','')} {data.get('provincia','')}</td></tr>
            <tr><td style="padding:3px 0;color:#666;">Partecipanti</td><td style="padding:3px 0;font-weight:500;">{num_partecipanti}</td></tr>
            <tr><td style="padding:3px 0;color:#666;">Accompagnatori</td><td style="padding:3px 0;font-weight:500;">{num_accompagnatori}{accomp_nomi_str}</td></tr>"""

    html = f"""<div style="font-family:Arial,sans-serif;max-width:600px;margin:0 auto;color:#1a1a1a;">

  <div style="background:#6399e7;padding:28px 32px;border-radius:10px 10px 0 0;">
    <div style="color:#fff;font-size:22px;font-weight:700;">Scuola Galenica del Dr. Peter J&auml;ger</div>
    <div style="color:rgba(255,255,255,0.7);font-size:12px;margin-top:6px;letter-spacing:0.5px;">J&Auml;GER GALENICA</div>
  </div>

  <div style="background:#fff;padding:32px;border:1px solid #e0e0e0;border-top:none;border-radius:0 0 10px 10px;">

    <p style="font-size:17px;margin:0 0 8px;">Gentile <strong>{nome}</strong>,</p>
    <p style="font-size:14px;color:#555;line-height:1.7;margin:0 0 24px;">la tua iscrizione &egrave; stata ricevuta con successo. Siamo lieti di accoglierti alla <strong style="color:#1a1a1a;">Scuola di Galenica Peter J&auml;ger</strong> di Cortona.</p>

    <div style="background:#f5f7fa;border-radius:8px;padding:14px 18px;margin-bottom:12px;">
      <div style="font-size:11px;font-weight:600;color:#999;text-transform:uppercase;letter-spacing:1px;margin-bottom:6px;">Corso</div>
      <div style="font-size:15px;font-weight:600;color:#1a2e4a;">{corso}</div>
    </div>

    <div style="background:#f5f7fa;border-radius:8px;padding:14px 18px;margin-bottom:12px;">
      <div style="font-size:11px;font-weight:600;color:#999;text-transform:uppercase;letter-spacing:1px;margin-bottom:10px;">Dati personali</div>
      <table style="width:100%;font-size:13px;border-collapse:collapse;">
        <tr><td style="padding:3px 0;color:#666;width:40%;">Ruolo</td><td style="padding:3px 0;font-weight:500;">{ruolo}</td></tr>
        <tr><td style="padding:3px 0;color:#666;">Allergie / dieta</td><td style="padding:3px 0;font-weight:500;">{allergie_str}</td></tr>
      </table>
      {partecipanti_html}
    </div>

    <div style="background:#f5f7fa;border-radius:8px;padding:14px 18px;margin-bottom:12px;">
      <div style="font-size:11px;font-weight:600;color:#999;text-transform:uppercase;letter-spacing:1px;margin-bottom:10px;">Fatturazione</div>
      <table style="width:100%;font-size:13px;border-collapse:collapse;">
        {fatt_rows}
      </table>
    </div>

    <div style="border-left:3px solid #6399e7;padding:12px 16px;background:#f5f7fa;border-radius:0 8px 8px 0;margin-bottom:12px;">
      <p style="margin:0;font-size:13px;color:#555;line-height:1.7;">Per qualsiasi informazione, o se noti un errore nei dati inseriti, contattaci senza effettuare una nuova iscrizione: scrivi a <a href="mailto:iscrizioni@jagergalenica.it" style="color:#6399e7;">iscrizioni@jagergalenica.it</a> oppure chiama il <strong style="color:#1a1a1a;">+39 346 675 0960</strong>.</p>
    </div>

    <div style="background:#f5f7fa;border-radius:8px;padding:14px 18px;margin-bottom:28px;">
      <div style="font-size:11px;font-weight:600;color:#999;text-transform:uppercase;letter-spacing:1px;margin-bottom:10px;">Come arrivare</div>
      <p style="margin:0 0 8px;font-size:13px;color:#555;">Per informazioni su come raggiungere la sede:</p>
      <a href="https://galenica.my.canva.site/arrivare" style="display:block;font-size:13px;color:#6399e7;margin-bottom:8px;text-decoration:none;">&#8594; Guida con mappa e indicazioni</a>
      <a href="https://www.youtube.com/watch?v=ci_qf9yNlB8&feature=youtu.be" style="display:block;font-size:13px;color:#6399e7;text-decoration:none;margin-bottom:14px;">&#9654; Video del percorso su YouTube</a>
      <div style="border-left:3px solid #6399e7;padding:10px 12px;border-radius:0 8px 8px 0;background:#fff;">
        <p style="margin:0;font-size:13px;color:#555;line-height:1.6;">Se arrivi in <strong style="color:#1a1a1a;">treno</strong>, ricordati di confermare i tuoi orari di arrivo alla Signora Anna per il servizio navetta: <a href="tel:+393466750960" style="color:#6399e7;">+39 346 675 0960</a>.</p>
      </div>
    </div>

    <div style="padding-top:20px;border-top:1px solid #eee;margin-bottom:24px;">
      <p style="margin:0 0 16px;font-size:14px;color:#555;font-style:italic;">A presto a Cortona,</p>
      <table style="font-size:13px;border-collapse:collapse;">
        <tr>
          <td style="padding-right:32px;vertical-align:top;">
            <div style="font-weight:500;color:#1a1a1a;">Lorenzo J&auml;ger</div>
            <div style="font-size:12px;color:#999;margin-top:2px;">Titolare</div>
          </td>
          <td style="vertical-align:top;">
            <div style="font-weight:500;color:#1a1a1a;">Marco Ternelli</div>
            <div style="font-size:12px;color:#999;margin-top:2px;">Direttore Scientifico</div>
          </td>
        </tr>
      </table>
    </div>

    <div style="padding-top:20px;border-top:1px solid #eee;font-size:12px;color:#aaa;">
      <p style="margin:0 0 10px;">Scuola Galenica del Dr. Peter J&auml;ger &middot; Cortona (AR) &middot; <a href="https://jager-form.onrender.com" style="color:#aaa;text-decoration:none;">jager-form.onrender.com</a></p>
      <table style="font-size:12px;border-collapse:collapse;">
        <tr>
          <td style="padding-right:16px;">
            <a href="https://www.facebook.com/corsigalenicajager" style="color:#aaa;text-decoration:none;display:flex;align-items:center;gap:5px;">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="#1877F2"><path d="M24 12.073C24 5.405 18.627 0 12 0S0 5.405 0 12.073C0 18.1 4.388 23.094 10.125 24v-8.437H7.078v-3.49h3.047V9.41c0-3.025 1.792-4.697 4.533-4.697 1.312 0 2.686.236 2.686.236v2.97h-1.513c-1.491 0-1.956.93-1.956 1.883v2.25h3.328l-.532 3.49h-2.796V24C19.612 23.094 24 18.1 24 12.073z"/></svg>
              Facebook
            </a>
          </td>
          <td>
            <a href="https://www.instagram.com/galenica.pratica/" style="color:#aaa;text-decoration:none;display:flex;align-items:center;gap:5px;">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="#E4405F"><path d="M12 2.163c3.204 0 3.584.012 4.85.07 3.252.148 4.771 1.691 4.919 4.919.058 1.265.069 1.645.069 4.849 0 3.205-.012 3.584-.069 4.849-.149 3.225-1.664 4.771-4.919 4.919-1.266.058-1.644.07-4.85.07-3.204 0-3.584-.012-4.849-.07-3.26-.149-4.771-1.699-4.919-4.92-.058-1.265-.07-1.644-.07-4.849 0-3.204.013-3.583.07-4.849.149-3.227 1.664-4.771 4.919-4.919 1.266-.057 1.645-.069 4.849-.069zM12 0C8.741 0 8.333.014 7.053.072 2.695.272.273 2.69.073 7.052.014 8.333 0 8.741 0 12c0 3.259.014 3.668.072 4.948.2 4.358 2.618 6.78 6.98 6.98C8.333 23.986 8.741 24 12 24c3.259 0 3.668-.014 4.948-.072 4.354-.2 6.782-2.618 6.979-6.98.059-1.28.073-1.689.073-4.948 0-3.259-.014-3.667-.072-4.947-.196-4.354-2.617-6.78-6.979-6.98C15.668.014 15.259 0 12 0zm0 5.838a6.162 6.162 0 1 0 0 12.324 6.162 6.162 0 0 0 0-12.324zM12 16a4 4 0 1 1 0-8 4 4 0 0 1 0 8zm6.406-11.845a1.44 1.44 0 1 0 0 2.881 1.44 1.44 0 0 0 0-2.881z"/></svg>
              @galenica.pratica
            </a>
          </td>
        </tr>
      </table>
    </div>

  </div>
</div>"""

    destinatari = [{"email": email_partecipante, "name": nome}]
    cc = [{"email": "iscrizioni@jagergalenica.it", "name": "Jager Galenica"}]

    payload = {
        "sender": {"name": "Scuola Galenica del Dr. Peter Jager", "email": "iscrizioni@jagergalenica.it"},
        "to": destinatari,
        "cc": cc,
        "subject": f"Conferma iscrizione — {corso}",
        "htmlContent": html
    }

    resp = requests.post(
        "https://api.brevo.com/v3/smtp/email",
        headers={
            "api-key": os.environ.get("BREVO_API_KEY", ""),
            "Content-Type": "application/json"
        },
        json=payload,
        timeout=10
    )
    if not resp.ok:
        print(f"Brevo error: {resp.text}")

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=port)

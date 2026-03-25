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
    
    if tipo_fatt == "farmacia":
        fatt_info = f"Farmacia/Azienda: {data.get('ragione_sociale','')}<br>P.IVA: {data.get('piva','')}<br>SDI: {data.get('sdi','')}"
    else:
        fatt_info = f"Privato<br>CF: {data.get('cf','')}<br>Indirizzo: {data.get('indirizzo','')} {data.get('cap','')} {data.get('citta','')} {data.get('provincia','')}"

    html = f"""
    <div style="font-family:Arial,sans-serif;max-width:600px;margin:0 auto;color:#1a1a1a;">
      <div style="background:#6399e7;padding:28px 32px;border-radius:10px 10px 0 0;">
        <div style="color:#fff;font-size:22px;font-weight:700;letter-spacing:0.04em;">JÄGER GALENICA</div>
        <div style="color:rgba(255,255,255,0.8);font-size:13px;margin-top:4px;">Scuola Galenica del Dr. Peter Jäger</div>
      </div>
      <div style="background:#fff;padding:32px;border:1px solid #e0e0e0;border-top:none;border-radius:0 0 10px 10px;">
        <p style="font-size:16px;margin-bottom:20px;">Gentile <strong>{nome}</strong>,</p>
        <p style="margin-bottom:24px;">la tua iscrizione è stata ricevuta con successo. Ti contatteremo a breve per conferma definitiva.</p>
        
        <div style="background:#f5f7fa;border-radius:8px;padding:20px;margin-bottom:20px;">
          <div style="font-size:12px;font-weight:600;color:#999;text-transform:uppercase;letter-spacing:0.08em;margin-bottom:12px;">Corso</div>
          <div style="font-size:15px;font-weight:600;color:#1a2e4a;">{corso}</div>
        </div>

        <div style="background:#f5f7fa;border-radius:8px;padding:20px;margin-bottom:20px;">
          <div style="font-size:12px;font-weight:600;color:#999;text-transform:uppercase;letter-spacing:0.08em;margin-bottom:12px;">Dati personali</div>
          <table style="width:100%;font-size:13px;border-collapse:collapse;">
            <tr><td style="padding:4px 0;color:#666;">Nome</td><td style="padding:4px 0;font-weight:500;">{nome}</td></tr>
            <tr><td style="padding:4px 0;color:#666;">Email</td><td style="padding:4px 0;font-weight:500;">{email_partecipante}</td></tr>
            <tr><td style="padding:4px 0;color:#666;">Telefono</td><td style="padding:4px 0;font-weight:500;">{data.get('telefono','')}</td></tr>
            <tr><td style="padding:4px 0;color:#666;">Ruolo</td><td style="padding:4px 0;font-weight:500;">{data.get('ruolo','')}</td></tr>
          </table>
        </div>

        <div style="background:#f5f7fa;border-radius:8px;padding:20px;margin-bottom:24px;">
          <div style="font-size:12px;font-weight:600;color:#999;text-transform:uppercase;letter-spacing:0.08em;margin-bottom:12px;">Fatturazione</div>
          <div style="font-size:13px;line-height:1.8;">{fatt_info}</div>
        </div>

        <p style="font-size:13px;color:#666;line-height:1.6;">Per qualsiasi informazione scrivi a <a href="mailto:iscrizioni@jagergalenica.it" style="color:#6399e7;">iscrizioni@jagergalenica.it</a> oppure chiama il <strong>+39 340 621 9415</strong>.</p>
        
        <div style="margin-top:28px;padding-top:20px;border-top:1px solid #eee;font-size:12px;color:#aaa;">
          Jäger Galenica SRLS · Cortona (AR) · corsigalenicajager.onrender.com
        </div>
      </div>
    </div>
    """

    # Email al partecipante
    destinatari = [{"email": email_partecipante, "name": nome}]
    # CC a Lorenzo e Anna
    cc = [
        {"email": "iscrizioni@jagergalenica.it", "name": "Jager Galenica"},
        {"email": "annajagermeco@gmail.com", "name": "Anna Jager"}
    ]

    payload = {
        "sender": {"name": "Jäger Galenica", "email": "iscrizioni@jagergalenica.it"},
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

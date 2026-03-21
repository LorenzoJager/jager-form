from flask import Flask, send_from_directory, jsonify, request
import requests
import os

app = Flask(__name__, static_folder='public')

AIRTABLE_TOKEN = os.environ.get("AIRTABLE_TOKEN", "")
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
    try:
        r = requests.post(
            f"https://api.airtable.com/v0/{BASE_ID}/{TABLE_ID}",
            headers={
                "Authorization": f"Bearer {AIRTABLE_TOKEN}",
                "Content-Type": "application/json"
            },
            json={"fields": fields},
            timeout=10
        )
        if r.ok:
            return jsonify({"success": True})
        else:
            return jsonify({"success": False, "error": r.text}), 500
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=port)

from flask import Flask, send_from_directory, jsonify
import requests
import os

app = Flask(__name__, static_folder='public')

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

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=port)

const express = require('express');
const fetch = require('node-fetch');
const path = require('path');

const app = express();
const PORT = process.env.PORT || 3000;

app.use(express.static(path.join(__dirname, 'public')));

// VIES proxy — avoids CORS from browser
app.get('/api/vies/:piva', async (req, res) => {
  const piva = req.params.piva.replace(/\D/g, '');
  if (piva.length !== 11) {
    return res.json({ isValid: false, error: 'Lunghezza P.IVA non valida' });
  }
  try {
    const url = `https://ec.europa.eu/taxation_customs/vies/rest-api/ms/IT/vat/${piva}`;
    const response = await fetch(url, { timeout: 8000 });
    const data = await response.json();
    res.json(data);
  } catch (err) {
    res.status(503).json({ isValid: false, error: 'VIES non raggiungibile', detail: err.message });
  }
});

// CAP lookup proxy
app.get('/api/cap/:cap', async (req, res) => {
  const cap = req.params.cap.replace(/\D/g, '');
  try {
    const url = `https://api.zippopotam.us/it/${cap}`;
    const response = await fetch(url, { timeout: 5000 });
    if (!response.ok) return res.json({});
    const data = await response.json();
    res.json(data);
  } catch (err) {
    res.json({});
  }
});

app.listen(PORT, () => {
  console.log(`Jager Galenica Form running on port ${PORT}`);
});

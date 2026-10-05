
# CipherLab Pro

A modern Flask dashboard for classical cryptography.

## Features
- Plain Text, Caesar Cipher and Vigenère Cipher conversion
- Encrypt/decrypt through source and destination selection
- Caesar shift and Vigenère key validation
- Live character mapping visualization
- Persistent local operation history in `history.json`
- Caesar brute-force / 26-shift cryptanalysis lab
- UTF-8 `.txt` upload and result download
- Algorithm knowledge page
- Responsive dark cybersecurity-style UI

## Run

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

Open `http://127.0.0.1:5000`.

This is an educational implementation of classical ciphers, not a replacement for modern authenticated encryption.

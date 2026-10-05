# 🔐 CipherLab Pro

A modern **Flask-based cryptography dashboard** for learning, experimenting with, and analyzing classical encryption algorithms.

CipherLab Pro provides an interactive cybersecurity-style interface for converting between **Plain Text, Caesar Cipher, and Vigenère Cipher**, with additional cryptanalysis and file-processing features.

## 🚀 Features

- 🔤 Plain Text ↔ Caesar Cipher conversion
- 🔑 Plain Text ↔ Vigenère Cipher conversion
- 🔄 Encryption and decryption
- 🎯 Caesar shift validation
- 🔐 Vigenère key validation
- 📊 Live character mapping visualization
- 🧪 Caesar Cipher brute-force / 26-shift analysis
- 📁 UTF-8 `.txt` file upload
- 💾 Download encrypted/decrypted results
- 📝 Local operation history
- 📚 Interactive algorithms knowledge page
- 🌙 Responsive cybersecurity-style dashboard

## 🛠️ Technologies

- **Python**
- **Flask**
- **HTML5**
- **CSS3**
- **JavaScript**
- **JSON**
- **REST API**

## 📂 Project Structure

```text
CipherLab-Pro/
│
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
│
├── static/
│   ├── app.js
│   └── style.css
│
└── templates/
    ├── index.html
    ├── history.html
    ├── bruteforce.html
    └── algorithms.html
```

## ⚙️ Installation

Clone the repository:

```bash
git clone https://github.com/ABDELRAHMAN2004-CYPER/cipher-converter.git
cd cipher-converter
```

Create a virtual environment:

```bash
python -m venv venv
```

Activate it on Windows:

```bash
venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the application:

```bash
python app.py
```

Then open:

```text
http://127.0.0.1:5000
```

## 🔬 Supported Algorithms

### Caesar Cipher

A classical substitution cipher where each letter is shifted by a fixed number of positions in the alphabet.

Example:

```text
Plain:  HELLO
Shift:  3
Cipher: KHOOR
```

### Vigenère Cipher

A polyalphabetic substitution cipher that uses a repeating key to determine the shift applied to each character.

Example:

```text
Plain:  HELLO
Key:    KEYKE
Cipher: RIJVS
```

## 🧪 Cryptanalysis Lab

CipherLab Pro includes a Caesar Cipher brute-force module that tests all **26 possible shifts** and displays the resulting plaintext candidates.

This demonstrates a fundamental concept in classical cryptanalysis: a cipher with a very small keyspace can be systematically attacked.

## 📁 File Processing

The application supports:

- `.txt` file upload
- Encryption/decryption of file contents
- UTF-8 text processing
- Result download

## 🔐 Security Note

CipherLab Pro is an **educational cryptography project** designed to demonstrate classical cryptographic concepts.

Caesar and Vigenère ciphers are historically important but are **not considered secure for modern applications**.

For real-world security, use modern authenticated encryption algorithms and established cryptographic libraries.

## 🎯 Project Purpose

The main goal of CipherLab Pro is to provide an interactive environment for understanding:

- Classical cryptography
- Encryption and decryption
- Key-based substitution
- Cryptanalysis
- Brute-force attacks
- Web application development with Flask
- Basic cybersecurity concepts

## 👨‍💻 Author

**Abdelrahman Elsaid**

Computer & Control Engineering  
Network & Cybersecurity Engineering

---

⭐ If you find this project useful for learning, consider giving it a star.
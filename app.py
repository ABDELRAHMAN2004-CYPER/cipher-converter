from flask import Flask, render_template, request, jsonify, send_file
from datetime import datetime
from pathlib import Path
import json
import io

app = Flask(__name__)

# =========================
# Paths
# =========================

BASE_DIR = Path(__file__).resolve().parent
HISTORY_FILE = BASE_DIR / "history.json"

# Create history.json if it doesn't exist
try:
    if not HISTORY_FILE.exists():
        HISTORY_FILE.write_text("[]", encoding="utf-8")
except PermissionError:
    print(f"ERROR: Cannot write to {HISTORY_FILE}")
    print("Move the project to a folder where you have write permission.")


# =========================
# History
# =========================

def load_history():
    if not HISTORY_FILE.exists():
        return []

    try:
        content = HISTORY_FILE.read_text(encoding="utf-8")

        if not content.strip():
            return []

        data = json.loads(content)

        return data if isinstance(data, list) else []

    except (json.JSONDecodeError, OSError):
        return []


def save_history(items):
    try:
        HISTORY_FILE.write_text(
            json.dumps(
                items[:100],
                ensure_ascii=False,
                indent=2
            ),
            encoding="utf-8"
        )

    except PermissionError:
        raise PermissionError(
            f"Cannot write to history file: {HISTORY_FILE}"
        )


# =========================
# Caesar Cipher
# =========================

def caesar(text, shift):
    shift %= 26

    out = []

    for ch in text:

        if 'A' <= ch <= 'Z':
            out.append(
                chr((ord(ch) - 65 + shift) % 26 + 65)
            )

        elif 'a' <= ch <= 'z':
            out.append(
                chr((ord(ch) - 97 + shift) % 26 + 97)
            )

        else:
            out.append(ch)

    return ''.join(out)


# =========================
# Vigenere Cipher
# =========================

def vigenere(text, key, decrypt=False):

    key = ''.join(
        c.lower()
        for c in key
        if c.isascii() and c.isalpha()
    )

    if not key:
        raise ValueError(
            "Vigenère key must contain at least one English letter."
        )

    out = []
    i = 0

    for ch in text:

        if ('A' <= ch <= 'Z') or ('a' <= ch <= 'z'):

            shift = ord(key[i % len(key)]) - 97

            if decrypt:
                shift = -shift

            base = 65 if ch.isupper() else 97

            out.append(
                chr((ord(ch) - base + shift) % 26 + base)
            )

            i += 1

        else:
            out.append(ch)

    return ''.join(out)


# =========================
# Convert To Plain
# =========================

def to_plain(text, source, shift=0, key=""):

    if source == "plain":
        return text

    if source == "caesar":
        return caesar(text, -int(shift))

    if source == "vigenere":
        return vigenere(text, key, True)

    raise ValueError("Invalid source algorithm.")


# =========================
# Convert From Plain
# =========================

def from_plain(text, target, shift=0, key=""):

    if target == "plain":
        return text

    if target == "caesar":
        return caesar(text, int(shift))

    if target == "vigenere":
        return vigenere(text, key, False)

    raise ValueError("Invalid target algorithm.")


# =========================
# Pages
# =========================

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/history")
def history_page():
    return render_template("history.html")


@app.route("/bruteforce")
def brute_page():
    return render_template("bruteforce.html")


@app.route("/algorithms")
def algorithms_page():
    return render_template("algorithms.html")


# =========================
# Convert API
# =========================

@app.post("/api/convert")
def api_convert():

    try:

        data = request.get_json(force=True)

        text = data.get("text", "")
        source = data.get("source", "plain")
        target = data.get("target", "caesar")

        shift = int(data.get("shift", 3))
        key = data.get("key", "")

        if not text:
            raise ValueError("Enter text before converting.")

        plain = to_plain(
            text,
            source,
            shift,
            key
        )

        result = from_plain(
            plain,
            target,
            shift,
            key
        )

        item = {
            "id": datetime.now().strftime("%Y%m%d%H%M%S%f"),
            "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "source": source,
            "target": target,
            "shift": shift,
            "key": key if (
                target == "vigenere"
                or source == "vigenere"
            ) else "",
            "input": text,
            "output": result
        }

        history = load_history()

        history.insert(0, item)

        save_history(history)

        return jsonify({
            "success": True,
            "result": result,
            "history": item
        })

    except Exception as e:

        return jsonify({
            "success": False,
            "error": str(e)
        }), 400


# =========================
# History API
# =========================

@app.get("/api/history")
def api_history():
    return jsonify(load_history())


@app.delete("/api/history")
def api_history_clear():

    save_history([])

    return jsonify({
        "success": True
    })


@app.delete("/api/history/<item_id>")
def api_history_delete(item_id):

    history = [
        x for x in load_history()
        if x.get("id") != item_id
    ]

    save_history(history)

    return jsonify({
        "success": True
    })


# =========================
# Caesar Brute Force
# =========================

@app.post("/api/bruteforce")
def api_bruteforce():

    try:

        text = request.get_json(force=True).get(
            "text",
            ""
        )

        if not text:
            raise ValueError(
                "Enter Caesar ciphertext first."
            )

        return jsonify({
            "success": True,
            "results": [
                {
                    "shift": s,
                    "text": caesar(text, -s)
                }
                for s in range(26)
            ]
        })

    except Exception as e:

        return jsonify({
            "success": False,
            "error": str(e)
        }), 400


# =========================
# File Upload
# =========================

@app.post("/api/file")
def api_file():

    try:

        f = request.files.get("file")

        if not f:
            raise ValueError(
                "Choose a .txt file."
            )

        text = f.read().decode("utf-8")

        return jsonify({
            "success": True,
            "text": text,
            "filename": f.filename
        })

    except UnicodeDecodeError:

        return jsonify({
            "success": False,
            "error": "Only UTF-8 text files are supported."
        }), 400

    except Exception as e:

        return jsonify({
            "success": False,
            "error": str(e)
        }), 400


# =========================
# Download
# =========================

@app.post("/api/download")
def api_download():

    data = request.get_json(force=True)

    content = data.get("text", "")

    filename = data.get(
        "filename",
        "cipher-result.txt"
    )

    return send_file(
        io.BytesIO(
            content.encode("utf-8")
        ),
        as_attachment=True,
        download_name=filename,
        mimetype="text/plain"
    )


# =========================
# Run
# =========================

if __name__ == "__main__":
    app.run(
        debug=True
    )
from flask import Flask, request, jsonify
import os
import requests

app = Flask(__name__)

# Берём OpenAI ключ из переменной окружения (чтобы не выкладывать на GitHub)
OPENAI_KEY = os.environ.get("OPENAI_KEY")

@app.route("/recognize", methods=["POST"])
def recognize():
    data = request.data
    if not data:
        return jsonify({"error": "No file provided"}), 400

    # Сохраняем временно WAV
    with open("temp.wav", "wb") as f:
        f.write(data)

    # Отправка на OpenAI Whisper
    url = "https://api.openai.com/v1/audio/transcriptions"
    headers = {
        "Authorization": f"Bearer {OPENAI_KEY}"
    }
    files = {
        "file": ("temp.wav", open("temp.wav", "rb")),
        "model": (None, "whisper-1")
    }

    try:
        r = requests.post(url, headers=headers, files=files)
        r.raise_for_status()
        transcription = r.json().get("text", "")
        return jsonify({"status": "ok", "transcription": transcription})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

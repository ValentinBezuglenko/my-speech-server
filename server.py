from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Поставьте свой API-ключ OpenAI
OPENAI_API_KEY = "YOUR_OPENAI_API_KEY"

@app.route("/recognize", methods=["POST"])
def recognize():
    if "file" not in request.files:
        return jsonify({"error": "No file provided"}), 400

    audio_file = request.files["file"]

    # Отправляем на OpenAI Whisper
    response = requests.post(
        "https://api.openai.com/v1/audio/transcriptions",
        headers={
            "Authorization": f"Bearer {OPENAI_API_KEY}"
        },
        files={
            "file": (audio_file.filename, audio_file.stream, "audio/wav")
        },
        data={
            "model": "whisper-1"
        }
    )

    if response.status_code != 200:
        return jsonify({"error": "Failed to recognize", "details": response.text}), 500

    return jsonify(response.json())

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

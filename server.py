from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

@app.route("/recognize", methods=["POST"])
def recognize():
    openai_key = request.headers.get("X-OPENAI-KEY")
    if not openai_key:
        return jsonify({"error": "Missing API key"}), 400

    if "file" not in request.files:
        return jsonify({"error": "No file provided"}), 400

    audio_file = request.files["file"]

    response = requests.post(
        "https://api.openai.com/v1/audio/transcriptions",
        headers={"Authorization": f"Bearer {openai_key}"},
        files={"file": (audio_file.filename, audio_file.stream, "audio/wav")},
        data={"model": "whisper-1"}
    )

    if response.status_code != 200:
        return jsonify({"error": "Failed to recognize", "details": response.text}), 500

    return jsonify(response.json())

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # берем порт из Render
    app.run(host="0.0.0.0", port=port)

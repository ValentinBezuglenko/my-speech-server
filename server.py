from flask import Flask, request, jsonify
import os

app = Flask(__name__)

@app.route("/recognize", methods=["POST"])
def recognize():
    # Берём сырые данные из POST
    data = request.data
    if not data:
        return jsonify({"error": "No file provided"}), 400

    # Сохраняем WAV временно (для теста)
    with open("temp.wav", "wb") as f:
        f.write(data)

    # Здесь можно добавить распознавание через OpenAI или любой другой сервис
    # Например, отправка temp.wav на Whisper API
    # Для теста просто возвращаем длину файла
    return jsonify({"status": "ok", "bytes_received": len(data)})

if __name__ == "__main__":
    # Получаем порт из переменной окружения Render
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

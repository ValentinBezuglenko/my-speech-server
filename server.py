from fastapi import FastAPI, UploadFile, File
import openai
import tempfile

app = FastAPI()

@app.post("/recognize")
async def recognize(file: UploadFile = File(...)):
    # временный файл
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
        tmp.write(await file.read())
        tmp_path = tmp.name

    # отправляем в OpenAI API
    with open(tmp_path, "rb") as audio_file:
        transcript = openai.audio.transcriptions.create(
            model="gpt-4o-mini-transcribe",  # дешево и быстро
            file=audio_file
        )

    return {"text": transcript.text}

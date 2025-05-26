import base64
import uuid
from gtts import gTTS
import os

def generar_audio(texto, filename="respuesta.mp3"):
    tts = gTTS(text=texto, lang="es")
    tts.save(filename)
    with open(filename, "rb") as f:
        audio_bytes = f.read()
    os.remove(filename)
    audio_b64 = base64.b64encode(audio_bytes).decode()
    audio_id = f"audio_{uuid.uuid4().hex}"
    return audio_b64, audio_id

import base64
import uuid
from gtts import gTTS
import os
import re  # nuevo: para limpiar texto

def limpiar_texto_para_audio(texto):
    # Quita los asteriscos (*) y reemplaza dobles con comillas si lo deseas
    texto = re.sub(r'\*+','\#+', '', texto)
    return texto

def generar_audio(texto, filename="respuesta.mp3"):
    texto_limpio = limpiar_texto_para_audio(texto)
    tts = gTTS(text=texto_limpio, lang="es")
    tts.save(filename)
    with open(filename, "rb") as f:
        audio_bytes = f.read()
    os.remove(filename)
    audio_b64 = base64.b64encode(audio_bytes).decode()
    audio_id = f"audio_{uuid.uuid4().hex}"
    return audio_b64, audio_id
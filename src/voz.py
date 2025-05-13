import speech_recognition as sr
from gtts import gTTS
from pydub import AudioSegment
from pydub.playback import play
import tempfile
import os

# Reproducir audio con gTTS y playsound
def hablar(texto):
    try:
        tts = gTTS(text=texto, lang='es')
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
            temp_file_path = fp.name
            tts.save(temp_file_path)

        audio = AudioSegment.from_mp3(temp_file_path)
        play(audio)
        os.remove(temp_file_path)
    except Exception as e:
        print(f"Error al reproducir voz: {e}")

def escuchar_microfono():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Escuchando...")
        audio = recognizer.listen(source)  # escucha indefinidamente hasta que termine de hablar
    try:
        return recognizer.recognize_google(audio, language="es-ES")
    except sr.UnknownValueError:
        return ""
    
def generar_audio(texto, filename="respuesta.mp3"):
    """Genera archivo de audio pero no lo reproduce (para Streamlit Cloud)"""
    try:
        tts = gTTS(text=texto, lang='es')
        tts.save(filename)
        return filename
    except Exception as e:
        print(f"Error al generar audio: {e}")
        return None
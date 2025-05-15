from gtts import gTTS
    
def generar_audio(texto, filename="respuesta.mp3"):
    """Genera archivo de audio pero no lo reproduce (para Streamlit Cloud)"""
    try:
        tts = gTTS(text=texto, lang='es')
        tts.save(filename)
        return filename
    except Exception as e:
        print(f"Error al generar audio: {e}")
        return None
    

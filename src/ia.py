import os
import requests
from dotenv import load_dotenv

load_dotenv()

def consultar_ia(pregunta):
    api_key = os.getenv("OPENROUTER_API_KEY")
    model = os.getenv("OPENROUTER_API_MODEL")
    url = os.getenv("OPENROUTER_API_URL")

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://chatbot-voz.streamlit.app",
        "X-Title": "Chat Educativo de Voz"
    }

    data = {
        "model": model,
        "messages": [
            {"role": "system", "content": "Eres un asistente que da respuestas directas de forma informal pero amigable. Tu especialidad es la seguridad industrial. Proporciona información útil y práctica sobre cómo actuar en caso de accidentes. Además, recuerda que estás en Bolivia y debes indicar al usuario que llame al número de emergencia correspondiente en el país."},
            {"role": "user", "content": pregunta}
        ]
    }

    try:
        r = requests.post(url, headers=headers, json=data)
        r.raise_for_status()
        return r.json()["choices"][0]["message"]["content"]
    except Exception as e:
        return f"Ocurrió un error: {e}"
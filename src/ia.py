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
            {
                "role": "system",
                "content": (
                    "Eres un asistente de voz especializado en seguridad industrial, "
                    "enfocado en estudiantes de Ingeniería Industrial en Bolivia. "
                    "Responde de manera clara, directa, informal y amigable. "
                    "Proporciona información útil, práctica y relevante sobre la Ingeniería de Seguridad Industrial, "
                    "incluyendo definiciones, normativas, planes generales y ejemplos aplicados en Bolivia. "
                    "Puedes referenciar libros y materiales de la Universidad Mayor de San Simón s. "
                    "Evita respuestas extensas o demasiado técnicas; prioriza la comprensión y la utilidad para estudiantes."
                )
            },
            {"role": "user", "content": pregunta}
        ]
    }

    try:
        r = requests.post(url, headers=headers, json=data)
        r.raise_for_status()
        return r.json()["choices"][0]["message"]["content"]
    except Exception as e:
        return f"Ocurrió un error: {e}"
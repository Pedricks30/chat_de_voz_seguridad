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
                    "Eres un asistente de voz especializado en las normas de seguridad industrial bolivianas e internacionales, "
                    "enfocado en estudiantes de Ingeniería Industrial en Bolivia. "
                    "Responde de manera clara, directa, informal y amigable. "
                    "Proporciona información útil, práctica y relevante sobre la Ingeniería de Seguridad Industrial, puedes buscar la información en sitios como "
                    "ISO (https://www.iso.org), OSHA (https://www.osha.gov), NIOSH (https://www.cdc.gov/niosh/) o equivalentes. "
                    "Incluye definiciones, normativas, planes generales y ejemplos aplicados en Bolivia. "
                    "Puedes referenciar libros y materiales de la Universidad Mayor de San Simón si es pertinente. "
                    "Evita respuestas extensas o demasiado técnicas; prioriza la comprensión y la utilidad para estudiantes.\n\n"

                    "Cuando se te pregunte por alguno de estos temas, responde con las normas correspondientes:\n"
                    "a) Prevención y combate contra incendios:\n"
                    "• Norma boliviana NB-13810 o equivalente.\n"
                    "• Norma internacional ISO/TS 11602 o NFPA.\n\n"
                    "b) Equipos de protección personal (EPP):\n"
                    "• Normas NB sobre selección y certificación de EPP.\n"
                    "• Norma internacional ISO 20345 o ANSI Z87.1.\n\n"
                    "c) Trabajos en altura:\n"
                    "• Norma NB sobre trabajos verticales o similares.\n"
                    "• Normas OSHA 1926.501 o ISO 22846.\n\n"
                    "d) Calzado de seguridad industrial:\n"
                    "• Norma NB específica.\n"
                    "• Norma internacional EN ISO 20345.\n\n"
                    "e) Señalización de seguridad:\n"
                    "• Norma boliviana de señalización.\n"
                    "• Norma ISO 7010 o ANSI Z535.\n\n"
                    "f) Procedimientos ante accidentes y primeros auxilios:\n"
                    "• Normas nacionales de protocolos de emergencia.\n"
                    "• Norma internacional ISO 45001, guías de la OMS o Cruz Roja.\n\n"
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
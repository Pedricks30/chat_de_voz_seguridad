import os
import requests
from dotenv import load_dotenv

load_dotenv()

def consultar_ia_calculadora(datos_calculo):
    """Consulta a la IA para análisis de resultados de la calculadora"""
    api_key = os.getenv("OPENROUTER_API_KEY")
    model = os.getenv("OPENROUTER_API_MODEL")
    url = os.getenv("OPENROUTER_API_URL")

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://calculadora-seguridad.streamlit.app",
        "X-Title": "Calculadora de Seguridad Industrial"
    }

    prompt = f"""
    Eres un especialista en seguridad industrial. Analiza estos resultados y proporciona recomendaciones:
    - Índice de Frecuencia: {datos_calculo['if']}
    - Índice de Gravedad: {datos_calculo['ig']}
    - Índice de Incidencia: {datos_calculo['ii']}
    - Horas trabajadas: {datos_calculo['nr']}
    - Accidentes: {datos_calculo['accidentes']}
    
    Proporciona:
    1. Interpretación profesional de los índices
    2. Recomendaciones específicas para mejorar
    3. Normativas relevantes aplicables
    4. Ejemplos de buenas prácticas
    """

    data = {
        "model": model,
        "messages": [
            {
                "role": "system",
                "content": (
                    "Eres un experto en seguridad industrial con especialización en análisis de "
                    "indicadores de seguridad. Proporciona análisis detallados pero concisos, "
                    "con recomendaciones prácticas basadas en normas ISO, OSHA y NB."
                )
            },
            {"role": "user", "content": prompt}
        ]
    }

    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]
    except Exception as e:
        return f"Error al consultar la IA: {str(e)}"
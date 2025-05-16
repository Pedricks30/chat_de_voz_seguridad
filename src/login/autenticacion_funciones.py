import re
import streamlit as st
import requests
from functools import lru_cache
import os
import logging
from typing import Tuple, Optional
from dotenv import load_dotenv

# Configuración de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

# Configuración de APIs
MAILSO_API_KEY = os.getenv("MAILSO_API_KEY")
CAPTAINVERIFY_API_KEY = os.getenv("CAPTAINVERIFY_API_KEY")

CORREOS_VERIFICADOS_MANUALMENTE = {
    "eplopez-es@udabol.edu.bo",
    # agregar otros correos conocidos
}

@lru_cache(maxsize=1000)
def verificar_correo_existente(correo: str) -> Tuple[bool, Optional[str]]:
    if correo.lower() in CORREOS_VERIFICADOS_MANUALMENTE:
        return True, "Lista blanca manual"
    """Verifica si un correo existe usando APIs con política de fallback segura"""
    # 1. Intento con Mails.so (configuración correcta)
    try:
        response = requests.get(
            "https://api.mails.so/v1/validate",
            headers={'x-mails-api-key': MAILSO_API_KEY},
            params={'email': correo},
            timeout=3
        )
        if response.status_code == 200:
            data = response.json()
            logger.info(f"Respuesta Mails.so para {correo}: {data}")
            if data.get('is_valid', False):
                return True, "Mails.so"
            return False, "Mails.so (inválido)"
    except Exception as e:
        logger.error(f"Error Mails.so con {correo}: {str(e)}")

    # 2. Intento con CaptainVerify
    try:
        response = requests.get(
            "https://api.captainverify.com/verify",
            params={'email': correo, 'apikey': CAPTAINVERIFY_API_KEY},
            timeout=3
        )
        if response.status_code == 200:
            data = response.json()
            logger.info(f"Respuesta CaptainVerify para {correo}: {data}")
            if data.get('status') == 'valid':
                return True, "CaptainVerify"
            return False, "CaptainVerify (inválido)"
    except Exception as e:
        logger.error(f"Error CaptainVerify con {correo}: {str(e)}")

    # 3. Fallback seguro (NO aceptar por defecto)
    logger.warning(f"Fallo en verificación de {correo} - Rechazado por seguridad")
    return False, "Error en verificación"

def validar_correo_educativo(correo: str) -> bool:
    """Valida el correo institucional con verificación estricta"""
    # 1. Validación de patrón
    patron = r"^[a-zA-Z0-9_.+-]+@(est\.umss|umss|udabol)\.edu(\.bo)?$"
    if not re.match(patron, correo):
        logger.warning(f"Patrón no coincide: {correo}")
        return False
    
    # 2. Verificación de existencia
    es_valido, fuente = verificar_correo_existente(correo)
    
    if not es_valido:
        logger.warning(f"Correo no verificado: {correo} por {fuente}")
        st.error("Correo institucional no válido. Por favor, use un correo existente.")
    
    return es_valido

def configurar_sesion_autenticada(correo: str):
    """Configura la sesión solo para correos verificados"""
    dominio = correo.split('@')[1]
    
    if "udabol.edu" in dominio:
        institucion = "UDABOL"
        rol = "estudiante" if not 'admin' in correo.lower() else "admin"
    else:
        institucion = "UMSS"
        rol = "estudiante" if "est." in dominio else ("docente" if not 'admin' in correo.lower() else "admin")
    
    st.session_state.update({
        'authenticated': True,
        'user_email': correo,
        'user_name': correo.split('@')[0].replace('.', ' ').title(),
        'institucion': institucion,
        'rol': rol,
        'verificado_por': verificar_correo_existente(correo)[1]
    })
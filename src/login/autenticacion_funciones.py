import re
import streamlit as st
import logging
from typing import Dict, Set

# Configuración de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Constantes para dominios y roles
DOMINIOS_PERMITIDOS = {
    "est.umss.edu": {"institucion": "UMSS", "rol_base": "estudiante"},
    "umss.edu": {"institucion": "UMSS", "rol_base": "docente"},
    "udabol.edu.bo": {"institucion": "UDABOL", "rol_base": "estudiante"}
}

ADMIN_WHITELIST = {
    "admin@umss.edu",
    "admin@udabol.edu.bo"
}

def validar_correo_institucional(correo: str) -> bool:
    """Valida que el correo sea de los dominios permitidos"""
    dominio = correo.split('@')[-1].lower() if '@' in correo else ''
    
    if dominio not in DOMINIOS_PERMITIDOS:
        logger.warning(f"Dominio no permitido: {correo}")
        return False
    return True

def determinar_rol(correo: str) -> str:
    """Determina el rol basado en el correo y lista blanca de admins"""
    if correo.lower() in ADMIN_WHITELIST:
        return "admin"
    
    dominio = correo.split('@')[-1].lower()
    config = DOMINIOS_PERMITIDOS.get(dominio, {})
    return config.get("rol_base", "invitado")

def configurar_sesion_autenticada(correo: str):
    """Configura la sesión para usuarios autenticados"""
    dominio = correo.split('@')[-1].lower()
    config = DOMINIOS_PERMITIDOS.get(dominio, {})
    
    st.session_state.update({
        'authenticated': True,
        'user_email': correo,
        'user_name': correo.split('@')[0].replace('.', ' ').title(),
        'institucion': config.get("institucion", "Desconocida"),
        'rol': determinar_rol(correo)
    })
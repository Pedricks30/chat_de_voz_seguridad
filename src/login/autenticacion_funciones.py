import re
import streamlit as st
import logging

# Configuración de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

CORREOS_VERIFICADOS_MANUALMENTE = {
    "eplopez-es@udabol.edu.bo",
    # agregar otros correos conocidos
}

def validar_correo_institucional(correo: str) -> bool:
    """Valida que el correo sea de los dominios permitidos"""
    dominios_permitidos = r"@(est\.umss\.edu|udabol\.edu\.bo)$"
    if not re.search(dominios_permitidos, correo.lower()):
        logger.warning(f"Dominio no permitido: {correo}")
        return False
    return True

def configurar_sesion_autenticada(correo: str):
    """Configura la sesión para correos institucionales verificados"""
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
        'rol': rol
    })
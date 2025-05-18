import streamlit as st
from google_auth_st import add_auth
from .autenticacion_funciones import validar_correo_institucional, configurar_sesion_autenticada
from PIL import Image
import os


def login_con_google():
    
    # Autenticación con google-auth-st
    add_auth()  # Esto manejará todo el flujo OAuth
    
    # Verificación después de la autenticación
    if hasattr(st.session_state, 'email'):
        correo = st.session_state.email
        
        # Validar correo institucional
        if not validar_correo_institucional(correo):
            st.error("Solo se permiten correos @est.umss.edu o @udabol.edu.bo")
            st.session_state.clear()
            return False
        
        # Configurar sesión con tus funciones
        configurar_sesion_autenticada(correo)
        return True
    
    return False
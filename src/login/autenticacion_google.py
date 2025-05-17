import streamlit as st
from streamlit_oauth import OAuth2Component
from .autenticacion_funciones import validar_correo_institucional, configurar_sesion_autenticada
import os
from dotenv import load_dotenv
import jwt  # pip install pyjwt
import requests
from io import BytesIO
from PIL import Image

load_dotenv()

@st.cache_data
def cargar_imagen_perfil(url):
    """Carga la imagen de perfil desde URL con cache"""
    try:
        response = requests.get(url, timeout=5)
        return Image.open(BytesIO(response.content))
    except Exception:
        return Image.open("src/img/default-profile.png")
def login_con_google():
    # Configuración de OAuth2 para Google
    CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
    CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
    REDIRECT_URI = os.getenv("GOOGLE_REDIRECT_URI", "http://localhost:8501")
    
    # Configuración del proveedor OAuth2
    AUTHORIZE_ENDPOINT = "https://accounts.google.com/o/oauth2/v2/auth"
    TOKEN_ENDPOINT = "https://oauth2.googleapis.com/token"
    REVOKE_ENDPOINT = "https://oauth2.googleapis.com/revoke"

    # Crear componente OAuth2
    oauth2 = OAuth2Component(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        authorize_endpoint=AUTHORIZE_ENDPOINT,
        token_endpoint=TOKEN_ENDPOINT,
        refresh_token_endpoint=TOKEN_ENDPOINT,
        revoke_token_endpoint=REVOKE_ENDPOINT,
    )

    # Mostrar botón de Google
    result = oauth2.authorize_button(
        name="Iniciar sesión con Google",
        icon="https://static.vecteezy.com/system/resources/previews/022/613/027/non_2x/google-icon-logo-symbol-free-png.png",
        redirect_uri=REDIRECT_URI,
        scope="openid email profile",
        key="google_login",
        extras_params={"prompt": "select_account"},
        use_container_width=True,
    )

    if result:
        if 'token' in result:
            try:
                # Obtener información del usuario del token JWT
                id_token = result['token']['id_token']
                
                # Decodificar el token JWT (sin verificar firma para simplificar)
                # En producción deberías verificar la firma
                user_info = jwt.decode(id_token, options={"verify_signature": False})
                
                correo = user_info.get("email", "")
                st.session_state['user_info'] = user_info  # Guardar info del usuario
                
                if validar_correo_institucional(correo):
                    configurar_sesion_autenticada(correo)
                    st.rerun()
                else:
                    st.error("Solo se permite el acceso con correos institucionales (@est.umss.edu o @udabol.edu.bo)")
                    st.session_state.clear()
                    
            except Exception as e:
                st.error(f"Error al procesar la autenticación: {str(e)}")
                st.session_state.clear()
                
        elif 'error' in result:
            st.error(f"Error de autenticación: {result['error']}")
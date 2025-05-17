import streamlit as st
from streamlit_oauth import OAuth2Component
from .autenticacion_funciones import validar_correo_institucional, configurar_sesion_autenticada
import os
from dotenv import load_dotenv
import jwt
from PIL import Image
import requests
from io import BytesIO

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
    # Configuración OAuth2
    CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
    CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
    REDIRECT_URI = os.getenv("REDIRECT_URI", "https://your-app-name.streamlit.app")  # Ajusta esta URL
    
    # Configuración simplificada sin revoke endpoint
    oauth2 = OAuth2Component(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        authorize_endpoint="https://accounts.google.com/o/oauth2/v2/auth",
        token_endpoint="https://oauth2.googleapis.com/token",
        refresh_token_endpoint="https://oauth2.googleapis.com/token",
        # Eliminamos el revoke endpoint que causaba el error
    )

    # Botón personalizado
    st.markdown("""
    <style>
        .google-btn {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            background-color: #4285F4;
            color: white;
            border-radius: 4px;
            padding: 10px 16px;
            border: none;
            font-family: 'Roboto', sans-serif;
            font-size: 14px;
            font-weight: 500;
            cursor: pointer;
            width: 100%;
            margin: 10px 0;
            transition: background-color 0.3s;
        }
        .google-btn:hover {
            background-color: #3367D6;
            color: white;
        }
        .google-icon {
            margin-right: 10px;
            height: 18px;
        }
    </style>
    <button onclick="document.getElementById('google-auth').click()" class="google-btn">
        <img src="https://upload.wikimedia.org/wikipedia/commons/5/53/Google_%22G%22_Logo.svg" class="google-icon">
        Iniciar sesión con Google
    </button>
    """, unsafe_allow_html=True)

    # Botón real oculto
    result = oauth2.authorize_button(
        name="",
        icon="",
        redirect_uri=REDIRECT_URI,
        scope="openid email profile",
        key="google_login",
        extras_params={"prompt": "select_account"},
        use_container_width=True,
    )

    if result and 'token' in result:
        try:
            id_token = result['token']['id_token']
            user_info = jwt.decode(id_token, options={"verify_signature": False})
            
            correo = user_info.get("email", "")
            st.session_state['user_info'] = user_info
            
            if validar_correo_institucional(correo):
                configurar_sesion_autenticada(correo)
                st.rerun()
            else:
                st.error("Solo se permiten correos @est.umss.edu o @udabol.edu.bo")
                st.session_state.clear()
                
        except Exception as e:
            st.error(f"Error al procesar la autenticación: {str(e)}")
            st.session_state.clear()
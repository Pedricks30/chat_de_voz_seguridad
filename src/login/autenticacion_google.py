import streamlit as st
from .autenticacion_funciones import validar_correo_institucional, configurar_sesion_autenticada
import os
from dotenv import load_dotenv
import jwt
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
    CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
    CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
    REDIRECT_URI = os.getenv("GOOGLE_REDIRECT_URI", "http://localhost:8501")
    
    # Mostrar botón de Google con estilo rojizo y padding ajustado
    st.markdown(f"""
    <style>
        .google-btn-custom {{
            display: inline-flex;
            align-items: center;
            justify-content: center;
            background-color: #EF5350;
            color: white;
            border-radius: 4px;
            padding: 0.6rem 1.2rem;  /* Padding aumentado */
            border: none;
            font-family: inherit;
            font-size: 1rem;
            font-weight: 400;
            cursor: pointer;
            width: 100%;
            margin: 0.5rem 0;
            text-decoration: none;
            white-space: nowrap;  /* Evita el salto de línea */
        }}
        .google-btn-custom:hover {{
            background-color: #E53935;
            color: white;
        }}
        .google-icon-custom {{
            height: 1.2rem;
            margin-right: 0.75rem;
            flex-shrink: 0;  /* Evita que el icono se reduzca */
        }}
    </style>
    """, unsafe_allow_html=True)

    auth_url = f"https://accounts.google.com/o/oauth2/v2/auth?client_id={CLIENT_ID}&redirect_uri={REDIRECT_URI}&response_type=code&scope=openid%20email%20profile&prompt=select_account"
    
    # Mostrar el botón centrado
    col1, col2, col3 = st.columns([1, 3, 1])  # Columna central más ancha
    with col2:
        st.markdown(f"""
        <a href="{auth_url}" target="_self">
            <button class="google-btn-custom">
                <img src="https://www.google.com/favicon.ico" 
                     class="google-icon-custom">
                Iniciar sesión con Google
            </button>
        </a>
        """, unsafe_allow_html=True)

    # Resto del código de manejo de callback...
    query_params = st.query_params
    if 'code' in query_params:
        try:
            code = query_params['code']
            
            # Intercambiar código por token
            token_url = "https://oauth2.googleapis.com/token"
            data = {
                'code': code,
                'client_id': CLIENT_ID,
                'client_secret': CLIENT_SECRET,
                'redirect_uri': REDIRECT_URI,
                'grant_type': 'authorization_code'
            }
            
            response = requests.post(token_url, data=data)
            response.raise_for_status()
            token_data = response.json()
            
            # Obtener información del usuario
            id_token = token_data['id_token']
            user_info = jwt.decode(id_token, options={"verify_signature": False})
            
            correo = user_info.get("email", "")
            st.session_state['user_info'] = user_info
            
            # Validar correo institucional y configurar sesión
            if validar_correo_institucional(correo):
                configurar_sesion_autenticada(correo)
                st.rerun()
            else:
                st.error("Solo se permite el acceso con correos institucionales (@est.umss.edu o @udabol.edu.bo)")
                st.session_state.clear()
                
        except Exception as e:
            st.error(f"Error al procesar la autenticación: {str(e)}")
            st.session_state.clear()
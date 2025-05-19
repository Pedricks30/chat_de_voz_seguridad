import streamlit as st
from .autenticacion_funciones import validar_correo_institucional, configurar_sesion_autenticada
import requests
import secrets
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests
from urllib.parse import urlencode

def generar_state_parameter():
    """Genera un state parameter único para protección CSRF"""
    state = secrets.token_hex(16)
    st.session_state.oauth_state = state
    return state

def verificar_state_parameter(state: str) -> bool:
    """Verifica que el state parameter coincida con el almacenado"""
    stored_state = st.session_state.pop('oauth_state', None)
    return stored_state is not None and stored_state == state

def login_con_google():
    try:
        CLIENT_ID = st.secrets["google_auth"]["client_id"]
        CLIENT_SECRET = st.secrets["google_auth"]["client_secret"]
        REDIRECT_URI = st.secrets["google_auth"]["redirect_uri"]
    except KeyError as e:
        st.error(f"Error de configuración: Falta {str(e)} en secrets.toml")
        st.stop()
    # Generar state parameter para protección CSRF
    state = generar_state_parameter()
    
    # Configuración del botón de Google
    st.markdown("""
    <style>
        .google-btn-custom {
            background-color: #EF5350 !important;
            color: white !important;
            border-radius: 4px;
            padding: 0.6rem 1.2rem;
            width: 100%;
            margin: 0.5rem 0;
            transition: background-color 0.3s;
        }
        .google-btn-custom:hover {
            background-color: #E53935 !important;
        }
    </style>
    """, unsafe_allow_html=True)

    # Construir URL de autenticación con state parameter
    auth_params = {
        "client_id": CLIENT_ID,
        "redirect_uri": REDIRECT_URI,
        "response_type": "code",
        "scope": "openid email profile",
        "access_type": "offline",
        "prompt": "select_account",
        "state": state
    }
    auth_url = f"https://accounts.google.com/o/oauth2/v2/auth?{urlencode(auth_params)}"
    
    # Mostrar botón de login
    st.markdown(f"""
    <a href="{auth_url}" target="_self">
        <button class="google-btn-custom">
            <img src="https://www.google.com/favicon.ico" style="height:1.2rem;margin-right:0.75rem;">
            Iniciar sesión con Google
        </button>
    </a>
    """, unsafe_allow_html=True)

    # Manejo del callback
    query_params = st.query_params
    if 'code' in query_params and 'state' in query_params:
        if not verificar_state_parameter(query_params['state']):
            st.error("Error de seguridad: State parameter no válido")
            st.session_state.clear()
            return False
        
        try:
            # Intercambiar código por token
            token_url = "https://oauth2.googleapis.com/token"
            token_data = {
                'code': query_params['code'],
                'client_id': CLIENT_ID,
                'client_secret': CLIENT_SECRET,
                'redirect_uri': REDIRECT_URI,
                'grant_type': 'authorization_code'
            }
            
            response = requests.post(token_url, data=token_data)
            response.raise_for_status()
            tokens = response.json()
            
            # Verificar token ID
            idinfo = id_token.verify_oauth2_token(
                tokens['id_token'],
                google_requests.Request(),
                CLIENT_ID
            )
            
            correo = idinfo['email']
            if not validar_correo_institucional(correo):
                st.error("Solo se permite acceso con correos institucionales autorizados")
                st.session_state.clear()
                return False
                
            # Configurar sesión
            st.session_state['user_info'] = {
                'email': idinfo['email'],
                'name': idinfo.get('name', correo.split('@')[0]),
                'picture': idinfo.get('picture', '')
            }
            configurar_sesion_autenticada(correo)
            st.rerun()
            
        except Exception as e:
            st.error(f"Error durante la autenticación: {str(e)}")
            st.session_state.clear()
            return False
    
    return st.session_state.get('authenticated', False)
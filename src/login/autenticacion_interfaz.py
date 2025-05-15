# Integración con correo corporativo
import smtplib
import streamlit as st

# Configuración de página
st.set_page_config(
    page_title="Intranet Corporativa",
    page_icon="🏢",
    layout="wide"
)

# Autenticación (reemplaza con tu sistema real)
def check_login():
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    
    if not st.session_state.authenticated:
        with st.sidebar:
            st.title("Acceso a la Intranet")
            username = st.text_input("Usuario")
            password = st.text_input("Contraseña", type="password")
            
            if st.button("Ingresar"):
                if username == "admin" and password == "password":  # Reemplaza con autenticación real
                    st.session_state.authenticated = True
                    st.rerun()
                else:
                    st.error("Credenciales incorrectas")
        st.stop()

check_login()
import streamlit as st
from .autenticacion_funciones import validar_correo_educativo, configurar_sesion_autenticada
from pathlib import Path
import time

def mostrar_login():
    """Interfaz de login mejorada con verificación de correos"""
    # Configuración de estilos
    st.markdown("""
    <style>
        header {visibility: hidden;}
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        .main .block-container {
            max-width: 800px;
            padding-top: 2rem;
        }
        .stTextInput>div>div>input {
            border-radius: 8px;
            padding: 10px;
            width: 100%;
        }
        .stButton>button {
            border-radius: 8px;
            padding: 10px;
            font-weight: 500;
            width: 100%;
        }
        .login-header {
            margin: 15px 0 5px 0;
            text-align: center;
        }
        .login-subtitle {
            color: #555;
            margin-bottom: 20px;
            text-align: left;
        }
        .verification-status {
            font-size: 0.9em;
            margin-top: 5px;
            color: #666;
        }
    </style>
    """, unsafe_allow_html=True)

    # Contenedor principal centrado
    col1, col2, col3 = st.columns([1, 4, 1])
    
    with col2:
        # Logo UMSS
        logo_path = Path(__file__).parent.parent / "img" / "logoumss.png"
        if logo_path.exists():
            st.image(str(logo_path), width=420)
        
        # Encabezado centrado y subtítulo alineado a la izquierda
        st.markdown("""
        <div class="login-header">
            <h3 style='color: #1a3e72;'>Acceso al Sistema de Seguridad Industrial</h3>
        </div>
        <p class="login-subtitle">Ingrese con su correo institucional</p>
        """, unsafe_allow_html=True)
        
        # Campo de correo alineado a la izquierda
        correo = st.text_input(
            "Correo electrónico",
            placeholder="usuario@est.umss.edu",
            label_visibility="collapsed"
        )
        
        # Botón de ingreso alineado a la izquierda
        if st.button("Ingresar", type="primary"):
            if not correo:
                st.error("Por favor ingrese su correo electrónico")
            elif not validar_correo_educativo(correo):
                st.error("Correo institucional no válido o no verificado")
            else:
                with st.spinner("Verificando credenciales..."):
                    time.sleep(1)  # Simular tiempo de verificación
                    configurar_sesion_autenticada(correo)
                    st.rerun()
        
        # Mensaje institucional centrado
        st.markdown("""
        <div style='text-align: center; margin-top: 30px; color: #666;'>
            <small>© 2025 Facultad de Ciencias y Tecnología - UMSS | Sistema de Seguridad Industrial </small>
        </div>
        """, unsafe_allow_html=True)

def verificar_autenticacion():
    """Verifica autenticación mostrando el login si es necesario"""
    if 'authenticated' not in st.session_state or not st.session_state.authenticated:
        mostrar_login()
        st.stop()
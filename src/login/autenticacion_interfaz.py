import streamlit as st
from pathlib import Path
from .autenticacion_google import login_con_google  # Importación relativa

def mostrar_login():
    """Interfaz de login simplificada con solo botón de Google"""
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
        .login-header {
            margin: 15px 0 5px 0;
            text-align: center;
        }
        .login-subtitle {
            color: #555;
            margin-bottom: 20px;
            text-align: center;
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
        
        # Encabezado y subtítulo
        st.markdown("""
        <div class="login-header">
            <h3 style='color: #1a3e72;'>Acceso al Sistema de Seguridad Industrial</h3>
        </div>
        <p class="login-subtitle">Ingrese con su cuenta institucional de Google</p>
        """, unsafe_allow_html=True)
        
        # Mostrar botón de Google
        login_con_google()
        
        # Mensaje institucional
        st.markdown("""
        <div style='text-align: center; margin-top: 30px; color: #666;'>
            <small>© 2025 Facultad de Ciencias y Tecnología - UMSS | Sistema de Seguridad Industrial</small>
        </div>
        """, unsafe_allow_html=True)

def verificar_autenticacion():
    """Verifica autenticación mostrando el login si es necesario"""
    if 'authenticated' not in st.session_state or not st.session_state.authenticated:
        mostrar_login()
        st.stop()
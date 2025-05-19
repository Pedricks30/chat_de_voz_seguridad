import streamlit as st
from pathlib import Path
from .autenticacion_google import login_con_google

def mostrar_login():
    """Interfaz de login con diseño mejorado y responsive"""
    st.markdown("""
    <style>
        .login-container {
            max-width: 450px;
            margin: 2rem auto;
            padding: 2rem;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        @media (max-width: 768px) {
            .login-container {
                margin: 1rem;
                padding: 1.5rem;
            }
        }
        .login-header {
            text-align: center;
            margin-bottom: 2rem;
        }
        .login-footer {
            text-align: center;
            margin-top: 2rem;
            color: #666;
            font-size: 0.85rem;
        }
    </style>
    """, unsafe_allow_html=True)

    with st.container():
        st.markdown('<div class="login-container">', unsafe_allow_html=True)
        
        # Logo responsivo (versión actualizada)
        logo_path = Path(__file__).parent.parent / "img" / "logoumss.png"
        if logo_path.exists():
            st.image(str(logo_path), use_container_width=True)  # Cambio realizado aquí
        
        # Encabezado
        st.markdown("""
        <div class="login-header">
            <h2 style='color: #1a3e72; margin-bottom: 0.5rem;'>Sistema de Seguridad Industrial</h2>
            <p style='color: #555; margin-top: 0;'>Acceso con cuenta institucional</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Autenticación
        if not login_con_google():
            st.stop()
        
        # Footer
        st.markdown("""
        <div class="login-footer">
            <small>© 2025 Facultad de Ciencias y Tecnología - UMSS</small>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)

def verificar_autenticacion():
    """Control de acceso con manejo de estado"""
    if not st.session_state.get('authenticated', False):
        mostrar_login()
        st.stop()
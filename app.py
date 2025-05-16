import streamlit as st
from src.login.autenticacion_interfaz import verificar_autenticacion
from src.chat_bot.chatbot_ui_interfaz import mostrar_interfaz_chatbot
from src.calculadora_indices.calculadora_interfaz import mostrar_interfaz_calculadora
from src.documentos.documentos_interfaz import mostrar_interfaz_documentos

def configurar_pagina():
    """Configuración común de la página"""
    st.set_page_config(
        page_title="Sistema de Seguridad Industrial",
        page_icon="🛡️",
        layout="centered",
        initial_sidebar_state="expanded"
    )
    
    # CSS personalizado (mantener tu estilo actual)
    st.markdown("""
    <style>
        /* Ajustes para móvil */
        @media (max-width: 768px) {
            .main .block-container {
                max-width: 95% !important;
                padding: 1rem;
            }
            
            [data-testid="stSidebar"] {
                width: 220px !important;
                padding: 0.5rem;
            }
        }
    </style>
    """, unsafe_allow_html=True)

def mostrar_sidebar():
    """Muestra el sidebar de navegación"""
    with st.sidebar:
        st.subheader("Módulos", divider=False)
        
        if st.session_state.get("is_admin"):
            if st.button("👨‍💼 Panel Admin", use_container_width=True):
                st.session_state.current_page = "admin"
        
        if st.button("🤖 Chatbot IA", use_container_width=True):
            st.session_state.current_page = "chatbot"
        
        if st.button("🧮 Calculadora de Índices", use_container_width=True):
            st.session_state.current_page = "calculadora"
        
        if st.button("📄 Documentos Corporativos", use_container_width=True):
            st.session_state.current_page = "documentos"
        
        st.divider()
        st.markdown(f"Usuario: {st.session_state.user_email}")
        if st.button("🚪 Salir", use_container_width=True):
            st.session_state.clear()
            st.rerun()

def main():
    # 1. Configuración de página (siempre primero)
    configurar_pagina()
    
    # 2. Verificar autenticación
    verificar_autenticacion()
    
    # 3. Configurar sidebar y routing
    mostrar_sidebar()
    
    # Lógica de routing
    if "current_page" not in st.session_state:
        st.session_state.current_page = "chatbot"
    
    if st.session_state.current_page == "chatbot":
        mostrar_interfaz_chatbot()
    elif st.session_state.current_page == "calculadora":
        mostrar_interfaz_calculadora()
    elif st.session_state.current_page == "documentos":
        mostrar_interfaz_documentos()
    elif st.session_state.current_page == "admin":
        st.title("Panel de Administración")
        st.write("Funcionalidades administrativas aquí")

if __name__ == "__main__":
    main()
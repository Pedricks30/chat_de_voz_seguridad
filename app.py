import streamlit as st
from src.chat_bot.chatbot_ui_interfaz import mostrar_interfaz_chatbot
from src.calculadora_indices.calculadora_interfaz import mostrar_interfaz_calculadora
from src.documentos.documentos_interfaz import mostrar_interfaz_documentos
from PIL import Image

def configurar_pagina():
    """Configuración de la página"""
    st.set_page_config(
        page_title="Sistema de Seguridad Industrial",
        page_icon=Image.open("src/img/iconoumss.png"),
        layout="centered",
        initial_sidebar_state="expanded"
    )
    
    st.markdown("""
    <style>
        .user-profile {
            display: flex;
            align-items: center;
            gap: 15px;
            margin-bottom: 20px;
        }
        .user-avatar {
            border-radius: 50%;
            width: 60px;
            height: 60px;
            object-fit: cover;
            border: 2px solid #1a3e72;
        }
        .user-info {
            flex: 1;
        }
        .user-name {
            font-weight: 600;
            margin-bottom: 0;
        }
    </style>
    """, unsafe_allow_html=True)

def mostrar_sidebar():
    """Sidebar simplificado sin autenticación"""
    with st.sidebar:
        # Mostrar logo o información básica
        st.markdown("""
        <div class="user-profile">
            <img src="src/img/iconoumss.png" class="user-avatar">
            <div class="user-info">
                <div class="user-name">Sistema de Seguridad</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.divider()
        
        # Menú de navegación
        st.subheader("Módulos")
        paginas = {
            "🤖 Chatbot IA": "chatbot",
            "🧮 Calculadora": "calculadora",
            "📄 Documentos": "documentos"
        }
        
        for texto, pagina in paginas.items():
            if st.button(texto, use_container_width=True):
                st.session_state.current_page = pagina
        
        # Opcional: Mantener panel admin si es necesario
        if st.session_state.get('rol') == 'admin':
            st.divider()
            if st.button("👨‍💼 Panel Admin", use_container_width=True):
                st.session_state.current_page = "admin"

def main():
    # Configuración inicial
    configurar_pagina()
    
    # Mostrar sidebar y contenido principal
    mostrar_sidebar()
    
    # Routing
    pagina = st.session_state.get('current_page', 'chatbot')
    if pagina == "chatbot":
        mostrar_interfaz_chatbot()
    elif pagina == "calculadora":
        mostrar_interfaz_calculadora()
    elif pagina == "documentos":
        mostrar_interfaz_documentos()
    elif pagina == "admin":
        st.title("Panel de Administración")

if __name__ == "__main__":
    main()
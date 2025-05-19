import streamlit as st
from src.chat_bot.chatbot_ui_interfaz import mostrar_interfaz_chatbot
from src.calculadora_indices.calculadora_interfaz import mostrar_interfaz_calculadora
from src.documentos.documentos_interfaz import mostrar_interfaz_documentos
import os
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
        /* Estilos para los botones del sidebar */
        .stButton>button {
            width: 100%;
            justify-content: left;
            padding: 0.5rem 1rem;
        }
        /* Ajustes para el título de los módulos */
        .sidebar .sidebar-content .stSubheader {
            font-size: 1.1rem;
            margin-bottom: 0.5rem;
        }
        /* Estilo para el div del nombre del sistema */
        .system-name {
            font-weight: 600;
            font-size: 1rem;
            text-align: center;
            margin: 1rem 0;
        }
        /* Sidebar a la mitad en móviles */
        @media (max-width: 768px) {
            section[data-testid="stSidebar"] {
                width: 50% !important;
                min-width: 200px !important;
            }
        }        
    </style>
    """, unsafe_allow_html=True)

def mostrar_sidebar():
    """Sidebar simplificado sin icono"""
    with st.sidebar:
        # Solo el nombre del sistema centrado
        st.markdown("<div class='system-name'>Sistema de Seguridad</div>", unsafe_allow_html=True)
        
        st.divider()
        
        # Menú de navegación
        st.subheader("Módulos")
        paginas = {
            "🤖 Chatbot IA": "chatbot",
            "🧮 Calculadora de Indices": "calculadora",
            "📄 Biblioteca UMSS": "documentos"
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
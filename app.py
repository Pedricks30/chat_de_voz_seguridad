import streamlit as st
from src.login.autenticacion_interfaz import verificar_autenticacion
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
        .user-email {
            font-size: 0.8rem;
            color: #666;
        }
        .user-institution {
            font-size: 0.8rem;
            color: #1a3e72;
            display: flex;
            align-items: center;
            gap: 5px;
        }
    </style>
    """, unsafe_allow_html=True)

def mostrar_sidebar():
    """Sidebar con perfil de usuario"""
    with st.sidebar:
        if st.session_state.get('authenticated'):
            user_info = st.session_state.get('user_info', {})
            
            st.markdown(f"""
            <div class="user-profile">
                <img src="{user_info.get('picture', 'src/img/default-profile.png')}" 
                     class="user-avatar" 
                     onerror="this.src='src/img/default-profile.png'">
                <div class="user-info">
                    <div class="user-name">{user_info.get('name', st.session_state.get('user_name', 'Usuario'))}</div>
                    <div class="user-email">{st.session_state.get('user_email', '')}</div>
                    <div class="user-institution">🔹 {st.session_state.get('institucion', '')}</div>
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
        
        if st.session_state.get('rol') == 'admin':
            if st.button("👨‍💼 Panel Admin", use_container_width=True):
                st.session_state.current_page = "admin"
        
        if st.session_state.get('authenticated'):
            st.divider()
            if st.button("🚪 Cerrar sesión", type="secondary", use_container_width=True):
                st.session_state.clear()
                st.rerun()

def main():
    configurar_pagina()
    verificar_autenticacion()
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
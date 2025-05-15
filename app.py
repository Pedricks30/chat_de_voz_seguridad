import streamlit as st
from src.chat_bot.chatbot_ui_interfaz import mostrar_interfaz_chatbot
from src.calculadora_indices.calculadora_interfaz import mostrar_interfaz_calculadora

def main():
    st.set_page_config(
        page_title="Sistema de Seguridad Industrial",
        page_icon="🛡️",
        layout="centered",
        initial_sidebar_state="expanded"
    )
    
    # CSS personalizado mejorado
    st.markdown("""
    <style>
        /* Contenedor principal */
        .main .block-container {
            max-width: 800px;
            padding-top: 1rem;
            padding-bottom: 1rem;
        }
        
        /* Sidebar estilizado */
        [data-testid="stSidebar"] {
            width: 280px !important;
            padding: 1.5rem;
        }
        
        /* Estilo para los botones */
        .stButton>button {
            width: 100%;
            border-radius: 8px;
            padding: 0.75rem;
            margin: 0.25rem 0;
            transition: all 0.2s;
        }
        
        .stButton>button:hover {
            background-color: 222831;
        }
        
        /* Mensajes de chat */
        [data-testid="stChatMessage"] {
            max-width: 85%;
            margin-left: auto;
            margin-right: auto;
        }
        
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
    
    # Sidebar con navegación mejorada
    with st.sidebar:
   #     st.title("Navegación")
        
        # Menú principal
        #if st.button("🏠 Inicio", use_container_width=True):
      #      st.session_state.current_page = "inicio"
       # st.divider()
        
        # Módulos
        st.subheader("Módulos", divider=False)
        if st.button("🤖 Chatbot IA", use_container_width=True):
            st.session_state.current_page = "chatbot"
        
        if st.button("🧮 Calculadora de Indices", use_container_width=True):
            st.session_state.current_page = "calculadora"
        
        if st.button("📊 Normas de Seguridad", use_container_width=True):
            st.session_state.current_page = "reportes"
        st.divider()
        
        # Enlaces externos
        st.subheader("Recursos", divider=False)
        st.markdown("[📚 Documentación](https://www.google.com)")

#LOGICA DE ROUTING
    if "current_page" not in st.session_state:
        st.session_state.current_page = "chatbot"
    
    if st.session_state.current_page == "chatbot":
        mostrar_interfaz_chatbot()
    elif st.session_state.current_page == "calculadora":
        mostrar_interfaz_calculadora()
    elif st.session_state.current_page == "reportes":
        st.warning("Módulo en desarrollo")
   # elif st.session_state.current_page == "inicio":
   #     st.warning("Página de inicio en desarrollo")

if __name__ == "__main__":
    main()
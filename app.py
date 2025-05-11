import streamlit as st 
from dotenv import load_dotenv
from src.voz import hablar, escuchar_microfono
from src.ia import consultar_ia

load_dotenv()

st.set_page_config(page_title="Chatbot de Voz", page_icon="🧠")
st.title("🧠 Especialista en la Seguridad Industrial")

# Estilos CSS
st.markdown("""
<style>
.chat-message {
    padding: 10px 15px;
    border-radius: 10px;
    margin-bottom: 10px;
    max-width: 80%;
    word-wrap: break-word;
    font-size: 16px;
}
.chat-user {
    background-color: #ffe3e3;
    color: #333;
    align-self: flex-start;
    border-left: 5px solid #ff6b6b;
}
.chat-ai {
    background-color: #fff3cd;
    color: #333;
    align-self: flex-end;
    border-left: 5px solid #ffc107;
}
.chat-container {
    display: flex;
    flex-direction: column;
}
.custom-button {
    background-color: transparent;
    border: none;
    padding: 0;
}
</style>
""", unsafe_allow_html=True)

# Inicializar historial
if "historial" not in st.session_state:
    st.session_state.historial = []

# Verificar si el botón fue presionado
if st.session_state.get("hablar") or st.button("🎙️ Hablar", use_container_width=True):
    pregunta = escuchar_microfono()
    if pregunta:
        with st.spinner("Pensando..."):
            respuesta = consultar_ia(pregunta)

        hablar(respuesta)
        st.session_state.historial.append(("👤", pregunta))
        st.session_state.historial.append(("🤖", respuesta))
    else:
        st.warning("No se detectó una pregunta. Intenta de nuevo.")

# Mostrar historial con estilo tipo chat
st.markdown("---")
st.subheader("📜 Historial de conversación")
st.markdown('<div class="chat-container">', unsafe_allow_html=True)

for rol, texto in st.session_state.historial:
    clase = "chat-user" if rol == "👤" else "chat-ai"
    emoji = "🧑‍💬" if rol == "👤" else "🤖"
    st.markdown(f'<div class="chat-message {clase}">{emoji} {texto}</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

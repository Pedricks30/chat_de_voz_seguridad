import streamlit as st
from streamlit_mic_recorder import speech_to_text
from dotenv import load_dotenv
from src.voz import generar_audio
from src.ia import consultar_ia
import os
import base64
import uuid

load_dotenv()

# Configuración de página
st.set_page_config(page_title="Chatbot de Voz", page_icon="🧠")
st.title("🧠 Especialista en Seguridad Industrial")

# Inicialización de estado
if "historial" not in st.session_state:
    st.session_state.historial = []
if "last_audio_id" not in st.session_state:
    st.session_state.last_audio_id = ""

# Función para autoplay
def autoplay_audio(file_path: str):
    audio_id = f"audio_{str(uuid.uuid4())}"
    st.session_state.last_audio_id = audio_id
    
    with open(file_path, "rb") as f:
        data = f.read()
        b64 = base64.b64encode(data).decode()
        md = f"""
            <audio id="{audio_id}" autoplay style="display:none">
            <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
            </audio>
            <script>
                var audio = document.getElementById("{audio_id}");
                audio.play().catch(e => console.log("Autoplay prevented:", e));
            </script>
            """
        st.components.v1.html(md, height=0)

# Interfaz de usuario
st.subheader("🎤 Haz tu pregunta por voz")

# Widget de reconocimiento de voz
pregunta = speech_to_text(
    language='es',
    start_prompt="🎙️ Presiona para hablar",
    stop_prompt="🛑 Detener grabación",
    just_once=True,
    use_container_width=True,
    key='stt'
)

# Procesamiento de pregunta
if pregunta and pregunta != st.session_state.get("last_question", ""):
    st.session_state.last_question = pregunta
    st.session_state.historial.append({"role": "user", "content": pregunta})
    
    with st.spinner("Pensando..."):
        respuesta = consultar_ia(pregunta)
        st.session_state.historial.append({"role": "assistant", "content": respuesta})
        
        # Generar y reproducir audio
        audio_file = generar_audio(respuesta)
        if audio_file:
            autoplay_audio(audio_file)
            os.remove(audio_file)

# Mostrar historial usando componentes nativos
st.markdown("---")
st.subheader("📜 Historial de conversación")

for mensaje in st.session_state.historial:
    if mensaje["role"] == "user":
        with st.chat_message("user"):
            st.write(f"🧑‍💬: {mensaje['content']}")
    else:
        with st.chat_message("assistant"):
            st.write(f"🤖: {mensaje['content']}")

# Botón de respaldo para reproducción manual
if st.session_state.get("historial") and st.session_state.historial[-1]["role"] == "assistant":
    if st.button("🔊 Reproducir última respuesta", key="reproducir"):
        if st.session_state.last_audio_id:
            st.markdown(f"""
            <script>
                var audio = document.getElementById("{st.session_state.last_audio_id}");
                audio.play().catch(e => console.log("Play prevented:", e));
            </script>
            """, unsafe_allow_html=True)

# Nota informativa
st.info("""
ℹ️ **Nota:** 
1. Presiona el micrófono y habla claramente
2. Espera a que el asistente procese tu pregunta
3. La respuesta se reproducirá automáticamente
4. Si no escuchas audio, usa el botón "Reproducir última respuesta"
""")
import streamlit as st
from streamlit_mic_recorder import speech_to_text
import os
import base64
import uuid
from .ia import consultar_ia
from .voz import generar_audio

def autoplay_audio(file_path: str):
    audio_id = f"audio_{str(uuid.uuid4())}"
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
        return md, audio_id

def mostrar_interfaz_chatbot():
    """Chatbot con interfaz limpia y mensajes alineados a la izquierda"""
    
    # CSS personalizado (se mantiene igual)
    st.markdown("""
    <style>
        /* Alinear todos los mensajes a la izquierda */
        .stChatMessage {
            margin-left: 0 !important;
            margin-right: auto !important;
            max-width: 90% !important;
        }
        
        /* Estilo específico para mensajes de usuario */
        [data-testid="stChatMessage-user"] {
            margin-left: auto !important;
            margin-right: 0 !important;
        }
        
        /* Estilo para el área de entrada fija */
        .input-area {
            position: fixed;
            bottom: 0;
            left: 0;
            right: 0;
            background: white;
            padding: 10px 30px;
            border-top: 1px solid #ccc;
            z-index: 9999;
        }
        
        /* Ajuste de padding para no tapar mensajes */
        .main > div {
            padding-bottom: 120px;
        }
    </style>
    """, unsafe_allow_html=True)

    st.title("🧠 Especialista en Seguridad Industrial")

    # Inicialización de variables de sesión
    if "historial" not in st.session_state:
        st.session_state.historial = []
    if "last_audio_id" not in st.session_state:
        st.session_state.last_audio_id = ""
    if "last_question" not in st.session_state:
        st.session_state.last_question = ""

    # Contenedor principal para los mensajes
    chat_container = st.container()

    # Mostrar historial de mensajes (solo una vez)
    with chat_container:
        for mensaje in st.session_state.historial:
            with st.chat_message(mensaje["role"]):
                st.markdown(mensaje["content"])

    # Entrada de usuario (texto o voz)
    st.markdown('<div class="input-area">', unsafe_allow_html=True)
    col1, col2 = st.columns([5, 1])
    with col1:
        user_input = st.chat_input("Escribe tu pregunta aquí...", key="chat_input")
    with col2:
        pregunta_voz = speech_to_text(
            language='es',
            start_prompt="🎤 Hablar",
            stop_prompt="🛑 Detener",
            just_once=True,
            key='stt'
        )
    st.markdown('</div>', unsafe_allow_html=True)

    # Procesamiento de la pregunta
    pregunta = user_input or pregunta_voz
    if pregunta and pregunta != st.session_state.last_question:
        st.session_state.last_question = pregunta
        
        # Agregar pregunta al historial
        st.session_state.historial.append({"role": "user", "content": pregunta})
        
        # Mostrar solo la nueva pregunta inmediatamente
        with chat_container:
            with st.chat_message("user"):
                st.markdown(pregunta)

        with st.spinner("Pensando..."):
            respuesta = consultar_ia(pregunta)
            
            # Agregar respuesta al historial
            st.session_state.historial.append({"role": "assistant", "content": respuesta})
            
            # Mostrar solo la nueva respuesta
            with chat_container:
                with st.chat_message("assistant"):
                    st.markdown(respuesta)

            # Generar y reproducir audio
            audio_file = generar_audio(respuesta)
            if audio_file:
                md, audio_id = autoplay_audio(audio_file)
                st.session_state.last_audio_id = audio_id
                st.components.v1.html(md, height=0)
                os.remove(audio_file)

    # Botón para volver a reproducir (se mantiene igual)
    with st.container():
        if st.session_state.historial and st.session_state.historial[-1]["role"] == "assistant":
            if st.button("🔊 Detener audio", key="reproducir"):
                if st.session_state.last_audio_id:
                    st.markdown(f"""
                    <script>
                        var audio = document.getElementById("{st.session_state.last_audio_id}");
                        audio.play().catch(e => console.log("Play prevented:", e));
                    </script>
                    """, unsafe_allow_html=True)

        st.info("""
        ℹ️ **Nota:**
        1. Escribe tu pregunta o usa el micrófono
        2. Espera la respuesta del asistente
        3. La respuesta se reproduce automáticamente
        4. Si desea que pare el audio, haga clic en el botón "Detener audio"
        """)
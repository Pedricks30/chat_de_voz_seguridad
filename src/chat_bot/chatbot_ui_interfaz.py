import streamlit as st
from streamlit_mic_recorder import speech_to_text
from .ia import consultar_ia
from .voz import generar_audio


def autoplay_audio(audio_b64, audio_id):
    """Genera el HTML para reproducir audio automáticamente"""
    md = f"""
    <audio id="{audio_id}" autoplay style="display:none">
    <source src="data:audio/mp3;base64,{audio_b64}" type="audio/mp3">
    </audio>
    <script>
        var audio = document.getElementById("{audio_id}");
        audio.play().catch(e => console.log("Autoplay prevented:", e));
    </script>
    """
    return md


def mostrar_interfaz_chatbot():
    st.markdown("""
    <style>
        /* Alinear los mensajes */
        .stChatMessage {
            margin-left: 0 !important;
            margin-right: auto !important;
            max-width: 90% !important;
        }
        [data-testid="stChatMessage-user"] {
            margin-left: auto !important;
            margin-right: 0 !important;
        }

        /* Fijar la barra de entrada */
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

        /* Separación para que no se tape el contenido */
        .main > div {
            padding-bottom: 120px;
        }
    </style>
    """, unsafe_allow_html=True)

    st.title("🧠 Asistente de Seguridad Industrial")

    # Inicialización
    if "historial" not in st.session_state:
        st.session_state.historial = []
    if "last_audio_id" not in st.session_state:
        st.session_state.last_audio_id = ""
    if "last_question" not in st.session_state:
        st.session_state.last_question = ""

    chat_container = st.container()

    # Mostrar historial
    with chat_container:
        for mensaje in st.session_state.historial:
            with st.chat_message(mensaje["role"]):
                st.markdown(mensaje["content"])

    # Zona de entrada fija (chat + botones)
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

    pregunta = user_input or pregunta_voz
    if pregunta and pregunta != st.session_state.last_question:
        st.session_state.last_question = pregunta

        st.session_state.historial.append({"role": "user", "content": pregunta})
        with chat_container:
            with st.chat_message("user"):
                st.markdown(pregunta)

        with st.spinner("Pensando..."):
            respuesta = consultar_ia(pregunta)
            st.session_state.historial.append({"role": "assistant", "content": respuesta})
            with chat_container:
                with st.chat_message("assistant"):
                    st.markdown(respuesta)

            audio_b64, audio_id = generar_audio(respuesta)
            st.session_state.last_audio_id = audio_id
            st.components.v1.html(autoplay_audio(audio_b64, audio_id), height=0)

    # Detener audio manualmente
    with st.container():
        if st.session_state.historial and st.session_state.historial[-1]["role"] == "assistant":
            if st.button("🔊 Detener audio", key="detener_audio"):
                if st.session_state.last_audio_id:
                    st.markdown(f"""
                    <script>
                        var audio = document.getElementById("{st.session_state.last_audio_id}");
                        if (audio) {{
                            audio.pause();
                            audio.currentTime = 0;
                        }}
                    </script>
                    """, unsafe_allow_html=True)

        st.info("""
        ℹ️ **Instrucciones:**
        1. Escribe tu pregunta o usa el micrófono
        2. Espera la respuesta del asistente
        3. La respuesta se reproduce automáticamente
        4. Puedes detener el audio con el botón correspondiente
        """)

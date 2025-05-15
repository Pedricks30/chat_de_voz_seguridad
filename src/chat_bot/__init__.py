# Exporta las funciones principales
from .chatbot_ui_interfaz import mostrar_interfaz_chatbot
from .ia import consultar_ia
from .voz import generar_audio

__all__ = ['mostrar_interfaz_chatbot', 'consultar_ia', 'generar_audio']
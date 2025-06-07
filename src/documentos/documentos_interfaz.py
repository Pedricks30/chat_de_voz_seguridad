import streamlit as st

def configurar_estilos():
    """Estilos CSS para la sección de documentos"""
    st.markdown("""
    <style>
        .doc-card {
            border: 1px solid #e0e0e0;
            border-radius: 10px;
            padding: 15px;
            margin-bottom: 15px;
            transition: all 0.3s;
        }
        .doc-card:hover {
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
            border-color: #4285F4;
        }
        .doc-title {
            font-weight: 600;
            font-size: 18px;
            color: #202124;
            margin-bottom: 5px;
        }
        .doc-actions {
            display: flex;
            gap: 10px;
            margin-top: 10px;
        }
        .view-btn {
            background-color: #4285F4;
            color: white !important;
            padding: 6px 12px;
            border-radius: 4px;
            text-decoration: none;
            font-size: 14px;
        }
        .drive-btn {
            background-color: #34A853;
            color: white !important;
            padding: 6px 12px;
            border-radius: 4px;
            text-decoration: none;
            font-size: 14px;
        }
    </style>
    """, unsafe_allow_html=True)

def mostrar_interfaz_documentos():
    """Interfaz principal para los documentos"""
    configurar_estilos()
    
    st.title("📚 Biblioteca de Documentos UMSS")
    st.markdown("Accede a los materiales de estudio de Seguridad Industrial")
    
    # ENLACE A LA CARPETA COMPLETA (reemplaza con tu enlace real)
    CARPETA_DRIVE = "https://drive.google.com/drive/folders/1FoZrldwy3iDgyiV2dHqfbzBfPt2Xt17k?usp=sharing"
    st.markdown(f"""
    ### 📂 [Acceder a la carpeta completa en Google Drive]({CARPETA_DRIVE})
    """)


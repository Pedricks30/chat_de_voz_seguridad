# Página de documentos corporativos
def documents_section():
    st.header("📄 Documentos Corporativos")
    
    # Ejemplo: Lista de documentos (podrías conectar a Google Drive o similar)
    documentos = {
        "Manual de políticas": "https://example.com/manual.pdf",
        "Organigrama 2023": "https://example.com/organigrama.pdf",
        "Formularios HR": "https://example.com/formularios.zip"
    }
    
    for doc, link in documentos.items():
        st.markdown(f"[{doc}]({link})")
    
    # Subida de archivos (solo para usuarios autorizados)
    if st.session_state.get("user_role") == "admin":
        uploaded_file = st.file_uploader("Subir nuevo documento")
        if uploaded_file:
            st.success(f"Archivo {uploaded_file.name} subido correctamente")

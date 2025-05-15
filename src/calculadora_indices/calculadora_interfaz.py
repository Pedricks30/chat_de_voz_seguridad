import streamlit as st
from src.calculadora_indices.calculadora_funciones import (
    calcular_horas_reales,
    calcular_jornadas_perdidas,
    calcular_indice_frecuencia,
    calcular_indice_gravedad,
    calcular_indice_incidencia,
    interpretar_if,
    interpretar_ig
)

def configurar_estilos():
    """Configuración de estilos CSS para la calculadora"""
    st.markdown("""
    <style>
        .calculadora-section {
            border: 1px solid #e1e4e8;
            border-radius: 8px;
            padding: 16px;
            margin-bottom: 16px;
        }
        .resultado-box {
            background-color: #f0f2f6;
            border-radius: 8px;
            padding: 12px;
            margin: 8px 0;
        }
        .formula-box {
            background-color: #f8f9fa;
            border-radius: 5px;
            padding: 15px;
            margin: 10px 0;
            border-left: 4px solid #28a745;
        }
        .stNumberInput, .stRadio, .stSelectbox {
            margin-bottom: 12px;
        }
    </style>
    """, unsafe_allow_html=True)

def mostrar_interfaz_calculadora():
    """Función principal para mostrar la interfaz de la calculadora"""
    configurar_estilos()
    
    st.title("🧮 Calculadora de Índices de Seguridad Industrial")
    st.markdown("Calcula los principales indicadores de seguridad según estándares internacionales")
    
    # Sección 1: Configuración básica
    with st.expander("📅 Configuración de días laborales", expanded=True):
        col1, col2, col3 = st.columns(3)
        with col1:
            dias_mes = st.number_input("Días trabajados al mes", min_value=1, max_value=31, value=28)
        with col2:
            horas_dia = st.number_input("Horas trabajadas al día", min_value=1, max_value=24, value=8)
        with col3:
            meses_anio = st.number_input("Meses trabajados al año", min_value=1, max_value=12, value=12)
    
    # Sección 2: Datos de personal
    with st.expander("👥 Datos de personal"):
        col1, col2 = st.columns(2)
        with col1:
            trabajadores = st.number_input("Número total de trabajadores", min_value=1, value=15)
        with col2:
            accidentes = st.number_input("Número de accidentes incapacitantes", min_value=0, value=8)
    
    # Sección 3: Horas no laboradas
    with st.expander("⏸️ Horas no laboradas (ajustes)"):
        st.markdown("Ingrese las horas no trabajadas por diferentes motivos:")
        col1, col2, col3 = st.columns(3)
        with col1:
            nv = st.number_input("Horas de vacaciones", min_value=0, value=0)
        with col2:
            np = st.number_input("Horas por permisos", min_value=0, value=0)
        with col3:
            n_be = st.number_input("Horas por enfermedad", min_value=0, value=0)
    
    # Sección 4: Gravedad de accidentes
    with st.expander("⚠️ Gravedad de accidentes"):
        metodo_jornadas = st.radio(
            "Método para calcular jornadas perdidas:",
            ("Ingresar directamente", "Calcular por tipo de lesión"),
            horizontal=True
        )
        
        if metodo_jornadas == "Ingresar directamente":
            j2 = st.number_input("Jornadas perdidas totales (días)", min_value=0, value=0)
        else:
            col1, col2, col3 = st.columns(3)
            with col1:
                muertes = st.number_input("Número de muertes (6000 días c/u)", min_value=0, value=0)
            with col2:
                brazos = st.number_input("Pérdida de brazos (4500 días c/u)", min_value=0, value=0)
            with col3:
                piernas = st.number_input("Pérdida de piernas (3000 días c/u)", min_value=0, value=0)
            j2 = calcular_jornadas_perdidas(muertes, brazos, piernas)
            st.info(f"Jornadas perdidas calculadas: {j2:,} días")
    
    # Cálculos
    nr = calcular_horas_reales(dias_mes, horas_dia, trabajadores, meses_anio, nv, np, n_be)
    if_val = calcular_indice_frecuencia(accidentes, nr)
    ig_val = calcular_indice_gravedad(j2, nr)
    ii_val = calcular_indice_incidencia(accidentes, trabajadores)
    
    # Resultados
    st.markdown("---")
    st.subheader("📊 Resultados")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Índice de Frecuencia (IF)", f"{if_val:,.2f}", help=interpretar_if(if_val))
    with col2:
        st.metric("Índice de Gravedad (IG)", f"{ig_val:,.2f}", help=interpretar_ig(ig_val))
    with col3:
        st.metric("Índice de Incidencia (Ii)", f"{ii_val:,.2f}")
    
    st.metric("Horas realmente trabajadas (NR)", f"{nr:,.0f} horas")
    
    # Fórmulas (similar a tu ejemplo)
    st.markdown("---")
    st.subheader("📝 Fórmulas utilizadas")
    
    with st.expander("Ver fórmulas detalladas"):
        st.markdown("""
        **Fórmulas clave:**
        - **Índice de Frecuencia (IF):**
          - IF = (n × 10⁶) / NR
            - n = Número de accidentes incapacitantes
            - NR = Horas realmente trabajadas

        - **Índice de Gravedad (IG):**
          - IG = (J × 10⁶) / NR
            - J = Jornadas perdidas totales (J = J₁ + J₂)
            - J₁ = Muertes × 6000 + Pérdida de brazos × 4500 + Pérdida de piernas × 3000
            - J₂ = Jornadas perdidas por otras lesiones (días)
            - NR = Horas realmente trabajadas

        - **Índice de Incidencia (Ii):**
          - Ii = (n × 1000) / TP
            - n = Número de accidentes incapacitantes
            - TP = Número total de trabajadores expuestos al riesgo

        - **Cálculo de Horas:**
          - NT = Días trabajados × Horas trabajadas × Trabajadores × Meses trabajados
          - NR = NT - (Nv + Np + Nbe)
            - NT = Horas totales trabajadas
            - Nv = Horas no laboradas por vacaciones
            - Np = Horas no laboradas por permisos
            - Nbe = Horas no laboradas por enfermedad
            - NR = Horas realmente trabajadas
        """)
    
    st.markdown("---")
    st.caption("**Referencias:** Normas NB, ISO/TS 11602, ISO 20345, OSHA 1926.501, ISO 45001")
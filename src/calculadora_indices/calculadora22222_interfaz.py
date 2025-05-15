import streamlit as st
import pandas as pd
from PIL import Image

# Configuración de la página
st.set_page_config(
    page_title="Sistema de Índices de Seguridad Industrial",
    page_icon="🛡️",
    layout="wide"
)

# CSS personalizado
st.html("""
<style>
    div[data-testid="stVerticalBlockBorderWrapper"] {
        gap: 1rem;
    }
    div[data-testid="stMetric"] {
        background-color: #f0f2f6;
        border-radius: 10px;
        padding: 15px;
        border-left: 4px solid #0068c9;
    }
    div[data-testid="stMetricLabel"] p {
        font-size: 16px;
        color: #555;
    }
    div[data-testid="stMetricValue"] {
        font-size: 24px;
        font-weight: bold;
    }
    .formula-box {
        background-color: #f8f9fa;
        border-radius: 5px;
        padding: 15px;
        margin: 10px 0;
        border-left: 4px solid #28a745;
    }
    .interpretacion {
        background-color: #e6f7ff;
        border-radius: 5px;
        padding: 15px;
        margin: 10px 0;
        border-left: 4px solid #1890ff;
    }
</style>
""")

# Título y descripción
st.title("🛡️ Sistema de Cálculo de Índices de Seguridad Industrial")
st.markdown("""
Esta herramienta calcula los principales indicadores de seguridad industrial según los estándares internacionales,
incluyendo los ejemplos mostrados en los ejercicios prácticos.
""")

# Sidebar para selección de modo
with st.sidebar:
    st.header("Modo de Operación")
    modo_calculo = st.radio(
        "Seleccione el tipo de cálculo:",
        ("Empresa Individual", "Múltiples Sucursales"),
        index=0
    )

    st.markdown("---")
    st.info("""
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

# Función para calcular índices de una sola empresa
def calcular_empresa_individual():
    st.header("📋 Datos de la Empresa")
    
    with st.expander("🔍 Ver ejemplos de referencia", expanded=False):
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("""
            **Ejemplo Librería Bicentenario:**
            - Trabajadores: 15
            - Horas/día: 8
            - Días/mes: 28
            - Accidentes: 8/año
            """)
        with col2:
            st.markdown("""
            **Resultado esperado:**
            - NR: 40,320 h/año
            - IF: 198.41 ≈ 198
            """)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        trabajadores = st.number_input("Número total de trabajadores", min_value=1, value=15)
        horas_dia = st.number_input("Horas trabajadas al día", min_value=1, max_value=24, value=8)
    with col2:
        dias_mes = st.number_input("Días trabajados al mes", min_value=1, max_value=31, value=28)
        meses_anio = st.number_input("Meses trabajados al año", min_value=1, max_value=12, value=12)
    with col3:
        accidentes = st.number_input("Número de accidentes incapacitantes en el año", min_value=0, value=8)
    
    st.markdown("---")
    st.subheader("Horas No Laboradas (Ajustes)")
    col1, col2, col3 = st.columns(3)
    with col1:
        nv = st.number_input("Nv (Horas no laboradas por vacaciones)", min_value=0, value=0)
    with col2:
        np = st.number_input("Np (Horas no laboradas por permisos)", min_value=0, value=0)
    with col3:
        n_be = st.number_input("Nbe (Horas no laboradas por enfermedad)", min_value=0, value=0)
    
    st.markdown("---")
    st.subheader("📉 Datos de Gravedad de Accidentes")
    st.markdown("Ingrese las jornadas perdidas (J₂) o calcule automáticamente:")
    
    metodo_jornadas = st.radio(
        "Método para jornadas perdidas:",
        ("Ingresar directamente", "Calcular por tipo de lesión"),
        horizontal=True
    )
    
    if metodo_jornadas == "Ingresar directamente":
        j2 = st.number_input("J₂ - Jornadas perdidas totales (días)", min_value=0, value=0)
    else:
        col1, col2, col3 = st.columns(3)
        with col1:
            muertes = st.number_input("Número de muertes (6000 días c/u)", min_value=0, value=0)
        with col2:
            brazos = st.number_input("Pérdida de brazos (4500 días c/u)", min_value=0, value=0)
        with col3:
            piernas = st.number_input("Pérdida de piernas (3000 días c/u)", min_value=0, value=0)
        j2 = (muertes * 6000) + (brazos * 4500) + (piernas * 3000)
        st.info(f"J₂ calculado: {j2:,} días perdidos")
    
    # Cálculos
    st.markdown("---")
    st.subheader("🔢 Cálculos Intermedios")
    
    # Horas totales
    horas_totales = dias_mes * horas_dia * trabajadores * meses_anio
    # Horas realmente trabajadas
    nr = horas_totales - nv - np - n_be
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Horas totales trabajadas (NT)", f"{horas_totales:,.0f} h/año")
        st.metric("Horas no laboradas (Nv + Np + Nbe)", f"{nv + np + n_be:,.0f} h/año")
    with col2:
        st.metric("Horas realmente trabajadas (NR)", f"{nr:,.0f} h/año", delta=f"{(nr/horas_totales*100 if horas_totales>0 else 0):.1f}% del total")
    
    # Cálculo de índices
    if nr > 0:
        if_calculado = (accidentes * 1000000) / nr
        ig_calculado = (j2 * 1000000) / nr
    else:
        if_calculado = 0
        ig_calculado = 0
    
    st.markdown("---")
    st.subheader("📊 Resultados Finales")
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Índice de Frecuencia (IF)", f"{if_calculado:,.2f}",
                help="Número de accidentes con lesiones incapacitantes por cada millón de horas trabajadas")
    with col2:
        st.metric("Índice de Gravedad (IG)", f"{ig_calculado:,.2f}",
                help="Jornadas perdidas por cada millón de horas trabajadas")
    
    # Interpretación
    with st.expander("📝 Interpretación de Resultados", expanded=True):
        st.markdown("""
        **Índice de Frecuencia (IF):**
        - < 5: Excelente desempeño en seguridad
        - 5-15: Buen desempeño, oportunidades de mejora
        - 15-25: Requiere atención prioritaria
        - > 25: Situación crítica, revisión inmediata
        """)
        
        st.markdown("""
        **Índice de Gravedad (IG):**
        - < 100: Accidentes con baja severidad
        - 100-500: Severidad moderada
        - > 500: Alta severidad, revisar protocolos
        """)

# Función para cálculo de múltiples sucursales
def calcular_multiple_sucursales():
    st.header("🏢 Cálculo para Múltiples Sucursales")
    st.info("Ejemplo basado en la empresa Rocasur con sucursales en Argentina, Bolivia y Colombia")
    
    num_sucursales = st.number_input("Número de sucursales a evaluar", min_value=1, max_value=10, value=3)
    
    # Crear DataFrame para almacenar datos
    datos_sucursales = pd.DataFrame(columns=[
        'Sucursal', 'Trabajadores', 'Accidentes', 
        'Muertes', 'Brazos', 'Piernas', 'NR', 'IF', 'IG'
    ])
    
    # Contenedor para formularios dinámicos
    with st.form("form_sucursales"):
        cols = st.columns(4)
        for i in range(num_sucursales):
            with st.expander(f"Sucursal {i+1}", expanded=(i==0)):
                c1, c2 = st.columns(2)
                with c1:
                    nombre = st.text_input(f"Nombre sucursal {i+1}", value=f"Sucursal {i+1}")
                    trabajadores = st.number_input(f"Trabajadores {i+1}", min_value=1, value=200 if i==0 else 180 if i==1 else 260)
                    accidentes = st.number_input(f"Accidentes incapacitantes {i+1}", min_value=0, value=32 if i==0 else 18 if i==1 else 22)
                with c2:
                    st.markdown("**Gravedad de accidentes**")
                    muertes = st.number_input(f"Muertes (6000 días) {i+1}", min_value=0, value=2 if i==0 else 0 if i==1 else 3)
                    brazos = st.number_input(f"Pérdida brazos (4500 días) {i+1}", min_value=0, value=1 if i<2 else 0)
                    piernas = st.number_input(f"Pérdida piernas (3000 días) {i+1}", min_value=0, value=0 if i==0 else 1)
                
                # Cálculos para cada sucursal (simplificado)
                horas_semana = 48
                semanas_anio = 53
                nr = horas_semana * semanas_anio * trabajadores
                j2 = (muertes * 6000) + (brazos * 4500) + (piernas * 3000)
                if_val = (accidentes * 1000000) / nr if nr > 0 else 0
                ig_val = (j2 * 1000000) / nr if nr > 0 else 0
                
                datos_sucursales.loc[i] = [
                    nombre, trabajadores, accidentes, 
                    muertes, brazos, piernas, nr, if_val, ig_val
                ]
        
        submitted = st.form_submit_button("Calcular Índices")
    
    if submitted:
        st.markdown("---")
        st.subheader("📊 Resultados por Sucursal")
        
        # Mostrar tabla resumen
        st.dataframe(datos_sucursales.style.format({
            'NR': '{:,.0f}',
            'IF': '{:,.2f}',
            'IG': '{:,.2f}'
        }), use_container_width=True)
        
        # Gráficos comparativos
        col1, col2 = st.columns(2)
        with col1:
            st.bar_chart(datos_sucursales.set_index('Sucursal')['IF'], color="#ff4b4b")
            st.caption("Índice de Frecuencia por Sucursal")
        with col2:
            st.bar_chart(datos_sucursales.set_index('Sucursal')['IG'], color="#0068c9")
            st.caption("Índice de Gravedad por Sucursal")
        
        # Cálculo de promedios
        st.markdown("---")
        st.subheader("🌍 Resumen Global")
        
        total_trabajadores = datos_sucursales['Trabajadores'].sum()
        total_accidentes = datos_sucursales['Accidentes'].sum()
        total_nr = datos_sucursales['NR'].sum()
        total_j2 = datos_sucursales.apply(lambda x: (x['Muertes']*6000 + x['Brazos']*4500 + x['Piernas']*3000), axis=1).sum()
        
        if_global = (total_accidentes * 1000000) / total_nr if total_nr > 0 else 0
        ig_global = (total_j2 * 1000000) / total_nr if total_nr > 0 else 0
        
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Trabajadores", f"{total_trabajadores:,.0f}")
        col2.metric("IF Global", f"{if_global:,.2f}")
        col3.metric("IG Global", f"{ig_global:,.2f}")
        col3.metric("Ii (indice de incidencia) Global", f"{ig_global:,.2f}")

# Selección de modo de cálculo
if modo_calculo == "Empresa Individual":
    calcular_empresa_individual()
else:
    calcular_multiple_sucursales()

# Notas y referencias
st.markdown("---")
st.caption("""
**Referencias:**  
- Normas NB (Normas Bolivianas)  
- ISO/TS 11602 (Prevención de incendios)  
- ISO 20345 (Calzado de seguridad)  
- OSHA 1926.501 (Trabajos en altura)  
- ISO 45001 (Seguridad y salud ocupacional)
""")
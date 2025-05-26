# 📊 Chat de Voz de Seguridad Industrial

## Proyecto de Seguridad Industrial - Calculadora de Índices y Asistente Virtual

Este proyecto es una herramienta integral para el **cálculo y análisis de indicadores de seguridad industrial**, junto con un **asistente virtual especializado en normativas de seguridad**.  
Está desarrollado con **Python** y **Streamlit** para una interfaz web interactiva.

---

## 🧰 Componentes Principales

### 🔢 Calculadora de Índices de Seguridad
Módulo especializado para calcular los principales indicadores de seguridad industrial:

- **Índice de Frecuencia (IF):** Mide la tasa de accidentes en relación a las horas trabajadas.
- **Índice de Gravedad (IG):** Evalúa la severidad de los accidentes.
- **Índice de Incidencia (Ii):** Relaciona accidentes con el número de trabajadores.

**Características destacadas:**
- Calculadora avanzada de índices de seguridad.
- Cálculo automático de horas realmente trabajadas.
- Dos métodos para calcular jornadas perdidas (tipo de lesión o valor directo).
- Interpretación automática de resultados según estándares internacionales.
- Visualización clara de fórmulas utilizadas.

---

### 🤖 Asistente Virtual de Seguridad Industrial

Chatbot con capacidades de voz para consultas sobre normativas y seguridad industrial.

**Funcionalidades:**
- Reconocimiento de voz para preguntas.
- Respuestas con síntesis de voz.
- Especializado en normas bolivianas e internacionales.
- Capacidad para interpretar resultados de los índices calculados.
- Proporciona recomendaciones basadas en resultados.

**Conocimiento especializado en:**
- Normas **NB**, **ISO**, **OSHA**.
- Cálculo e interpretación de índices.
- Ejemplos prácticos y ejercicios resueltos.
- Protocolos de seguridad industrial.

---

### 📚 Biblioteca de Documentos Técnicos

Repositorio organizado con materiales de referencia:

- Acceso directo a documentos en **Google Drive**.
- Tarjetas organizadas por categorías.
- Visualización optimizada para dispositivos móviles.

---

## 🛠️ Estructura del Código

```
src/
├── app.py                       # Punto de entrada principal
├── calculadora_indices/
│   ├── calculadora_funciones.py     # Lógica de cálculo de índices
│   └── calculadora_interfaz.py      # Interfaz Streamlit de la calculadora
├── chat_bot/
│   ├── chatbot_ui_interfaz.py       # Interfaz del chatbot
│   ├── ia.py                        # Integración con IA (OpenRouter API)
│   └── voz.py                       # Funciones de síntesis de voz
├── documentos/
│   └── documentos_interfaz.py       # Interfaz de la biblioteca de documentos
└── img/
    └── iconoumss.png
```

---

## 💡 Buenas Prácticas Implementadas

- Estructura modular organizada por funcionalidad.
- Documentación clara con `docstrings` en funciones clave.
- Interfaz profesional con Streamlit y estilos CSS personalizados.
- Casos de uso reales documentados.
- Manejo de variables de entorno para claves API.
- Gestión de estado con `session_state`.
- Componentes reutilizables.

---

## 🚀 Cómo Ejecutar el Proyecto

### Pre-requisitos:

```bash
Python 3.8+
pip install -r requirements.txt
```

O puedes instalar manualmente:

```bash
pip install streamlit gtts python-dotenv requests streamlit-mic-recorder
```

---

### Configuración:

Crear archivo `.env` en la raíz del proyecto con las siguientes variables:

```env
OPENROUTER_API_KEY=tu_clave_api
OPENROUTER_API_MODEL=modelo_elegido
OPENROUTER_API_URL=https://api.openrouter.ai/v1/chat/completions
```

---

### Ejecución:

```bash
streamlit run app.py
```

---

## 📌 Notas para Futuros Proyectos

Este proyecto demuestra cómo integrar múltiples funcionalidades en una sola aplicación:

- Uso de APIs externas (como OpenRouter).
- Técnicas avanzadas de Streamlit (CSS, estado, audio).
- Modelo claro de documentación técnica.
- Ejemplos de cálculos complejos interpretados automáticamente.

---

### ✅ Este README incluye:

- Propósito del proyecto.
- Componentes principales.
- Estructura del código.
- Instrucciones de instalación y ejecución.
- Buenas prácticas.
- Lecciones aprendidas.

---

Desarrollado con ❤️ usando Python y Streamlit.

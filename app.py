import streamlit as st
import os
from dotenv import load_dotenv
from src.agent.assistant import UTPAssistantAgent

# Esto obliga a Python a buscar el archivo .env en la raíz y cargar las variables
load_dotenv(override=True)

st.set_page_config(page_title="UTP Assistant - UTPConsult", page_icon="🤖", layout="wide")

with st.sidebar:
    ruta_logo = "assets/utp_assistant_logo_dark.png"
    if os.path.exists(ruta_logo):
        st.image(ruta_logo, use_container_width=True)
    st.markdown("### Integrantes del Grupo")
    st.write("- Estudiante 1\n- Estudiante 2\n- Estudiante 3\n- Estudiante 4")

# Verificación de seguridad para evitar que la app se caiga si el archivo no existe
if os.path.exists(ruta_logo):
    st.image(ruta_logo, width=140)
else:
    # Si aún no tienes la imagen física, muestra un emoji como marcador de posición (placeholder)
    st.header("🤖") 

st.title("UTP Assistant — Consola de Control")
st.subheader("Simulador de Procesamiento de Correos")

# Verificar que la API Key esté cargada
if not os.getenv("GEMINI_API_KEY") or os.getenv("GEMINI_API_KEY") == "tu_api_key_aqui":
    st.error("Error de Configuración: No se encontró la variable `GEMINI_API_KEY` en el archivo `.env`. Por favor añádela para operar la IA.")
else:
    st.success("Conexión con la API de Gemini establecida correctamente (Esquema de Plan Gratuito).")

# Instanciar el agente de IA
@st.cache_resource
def obtener_agente():
    return UTPAssistantAgent()

try:
    agente = obtener_agente()
except Exception as e:
    st.error(f"Error al inicializar el agente: {e}")
    agente = None

col1, col2 = st.columns([1, 1])

with col1:
    st.markdown("### Bandeja de Entrada Semántica")
    st.caption("Pega el cuerpo del correo electrónico recibido para iniciar el análisis automático del Asistente.")
    
    ejemplo_correo = (
        "Hola equipo de UTP Consult, gracias por la propuesta. Nos interesa avanzar. "
        "¿Podríamos tener una reunión la próxima semana para discutir los detalles técnicos "
        "del módulo de pagos? Adjunto un documento con algunos requisitos iniciales. "
        "Saludos, Ana Torres de TechCorp."
    )

    # 1. Input para el Correo del Remitente
    correo_remitente_defecto = "ana.torres@techcorp.com"

    remitente_input = st.text_input(
        "Correo Electrónico del Remitente:",
        value=correo_remitente_defecto
    )

    # 2. Área de texto para el cuerpo del mensaje
    correo_input = st.text_area(
        "Cuerpo del Correo Electrónico:",
        value=ejemplo_correo,
        height=150
    )
    
    procesar_btn = st.button("Procesar Correo Entrante", type="primary")

with col2:
    st.markdown("### Monitoreo del Ciclo de Ejecución (Run)")
    
    if procesar_btn and agente:
        with st.spinner("El Asistente está analizando el flujo e intenciones..."):
            resultado = agente.procesar_correo(correo_input, remitente_input)
            
            # Mostrar Estado de Acciones
            if resultado["herramientas_invocadas"]:
                st.info("🔔 **Estado: `requires_action` detectado.** El modelo identificó parámetros válidos y solicitó invocar herramientas externas.")
                
                for exec_data in resultado["herramientas_invocadas"]:
                    with st.expander(f"🛠️ Función Invocada: `{exec_data['funcion']}`", expanded=True):
                        st.markdown("**Parámetros Extraídos por Gemini:**")
                        st.json(exec_data["parametros_extraidos"])
                        st.markdown("**Respuesta del Sistema Externo (Mock):**")
                        st.success(f"{exec_data['resultado']['herramienta']}: {exec_data['resultado']['msg']}")
            else:
                st.warning("**Estado: Ejecución directa sin herramientas.** La información fue muy ambigua o el correo no requería acciones automatizadas.")
            
            # Mostrar la respuesta en lenguaje natural o resumen operativo
            st.markdown("### Informe Interno de Respuesta Generado:")
            if resultado["respuesta_analista"]:
                st.write(resultado["respuesta_analista"])
            else:
                st.write("*El asistente ha procesado las solicitudes operativas tras bastidores de forma correcta.*")
    else:
        st.write("Esperando un correo entrante para iniciar el ciclo de vida del Run...")
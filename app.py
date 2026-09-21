import streamlit as st
import os
from dotenv import load_dotenv
from src.agent.assistant import UTPAssistantAgent

# Esto obliga a Python a buscar el archivo .env en la raíz y cargar las variables
load_dotenv(override=True)

st.set_page_config(page_title="UTP Assistant - UTPConsult", page_icon="assets/utp_assistant_icono.png", layout="wide")

# Verificación de seguridad para evitar que la app se caiga si el archivo no existe
ruta_logo = "assets/utp_assistant_logo_dark.png"
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

            # 1. Alerta de Estado General basada en el Status real de la API de Gemini
            if resultado["status"] == "requires_action":
                st.info("**Estado del Agente: `requires_action` detectado.** El modelo identificó parámetros válidos y coordinó las herramientas externas.")
            else:
                st.warning("**Estado del Agente: `success` síncrono directo.** Correo analizado sin requerimiento de ejecución de herramientas.")
            
            # Extraemos en una lista limpia los nombres de las funciones que la IA invocó en su historial
            funciones_ejecutadas = [exec_data["funcion"] for exec_data in resultado["herramientas_invocadas"]]
            
            st.markdown("#### Estado Individual de Integraciones")

            # --- CONTROL INDEPENDIENTE: JIRA ---
            if "crear_ticket_en_jira" in funciones_ejecutadas:
                data_jira = next(item for item in resultado["herramientas_invocadas"] if item["funcion"] == "crear_ticket_en_jira")
                with st.expander("Gestión de Requisitos (Jira Cloud) — EJECUTADO", expanded=True):
                    st.markdown("**Parámetros Extraídos por Gemini:**")
                    st.json(data_jira["parametros_extraidos"])
                    st.markdown("**Respuesta del Sistema Externo Sincronizado:**")
                    st.success(f"{data_jira['resultado']['herramienta']}: {data_jira['resultado']['msg']}")
            else:
                st.warning("**Gestión de Requisitos (Jira Cloud) — RETENIDO**\n\nEl correo no contiene solicitudes de desarrollo técnico o el remitente no requiere un caso de ingeniería.")

            # --- CONTROL INDEPENDIENTE: GOOGLE CALENDAR ---
            if "agendar_reunion_en_google_calendar" in funciones_ejecutadas:
                data_cal = next(item for item in resultado["herramientas_invocadas"] if item["funcion"] == "agendar_reunion_en_google_calendar")
                with st.expander("Gestión de Agenda (Google Calendar) — EJECUTADO", expanded=True):
                    st.markdown("**Parámetros Extraídos por Gemini:**")
                    st.json(data_cal["parametros_extraidos"])
                    st.markdown("**Respuesta del Sistema Externo Sincronizado:**")
                    st.success(f"{data_cal['resultado']['herramienta']}: {data_cal['resultado']['msg']}")
            else:
                st.warning("**Gestión de Agenda (Google Calendar) — RETENIDO**\n\nLa automatización fue bloqueada preventivamente por ambigüedad temporal o ausencia de marcas de tiempo concretas.")

            # --- CONTROL INDEPENDIENTE: CRM ---
            if "actualizar_contacto_en_crm" in funciones_ejecutadas:
                data_crm = next(item for item in resultado["herramientas_invocadas"] if item["funcion"] == "actualizar_contacto_en_crm")
                with st.expander("Gestión de Prospectos (CRM) — EJECUTADO", expanded=True):
                    st.markdown("**Parámetros Extraídos por Gemini:**")
                    st.json(data_crm["parametros_extraidos"])
                    st.markdown("**Respuesta del Sistema Externo Sincronizado:**")
                    st.success(f"{data_crm['resultado']['herramienta']}: {data_crm['resultado']['msg']}")
            else:
                st.warning("**Gestión de Prospectos (CRM) — RETENIDO**\n\nNo se requirió dar de alta un nuevo lead (remitente institucional o cliente existente).")

            # 3. Mostrar la respuesta formal en lenguaje natural
            st.markdown("---")
            st.markdown("### Informe Interno de Respuesta Generado:")
            if resultado["respuesta_analista"]:
                st.write(resultado["respuesta_analista"])
            else:
                st.write("*El asistente ha procesado las solicitudes operativas de forma correcta.*")
    else:
        st.write("Esperando un correo entrante para iniciar el ciclo de vida del Run...")

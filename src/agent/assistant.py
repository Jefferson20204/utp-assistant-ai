import os
from google import genai
from google.genai import types
from src.agent.prompts import SYSTEM_PROMPT
from src.tools.jira import crear_ticket_en_jira
from src.tools.google_calendar import agendar_reunion_en_google_calendar
from src.tools.crm import actualizar_contacto_en_crm

class UTPAssistantAgent:
    def __init__(self):
        # Inicializar el SDK oficial de Google GenAI usando la API Key cargada
        api_key = os.getenv("GEMINI_API_KEY")
        self.client = genai.Client(api_key=api_key)
        
        # Mapeo interno de funciones para ejecutar dinámicamente cuando el modelo lo solicite
        self.available_tools = {
            "crear_ticket_en_jira": crear_ticket_en_jira,
            "agendar_reunion_en_google_calendar": agendar_reunion_en_google_calendar,
            "actualizar_contacto_en_crm": actualizar_contacto_en_crm
        }
        
        # Configuración del agente inyectando las herramientas nativas de Python
        self.config = types.GenerateContentConfig(
            system_instruction=SYSTEM_PROMPT,
            tools=[crear_ticket_en_jira, agendar_reunion_en_google_calendar, actualizar_contacto_en_crm],
            temperature=0.1
        )
        
    def procesar_correo(self, cuerpo_correo: str, remitente_correo: str):
        """
        Empaqueta los metadatos del correo y solicita la generación de contenido
        e invocación de herramientas reales a la API de Gemini.
        """
        # ESTRATEGIA DE PROMPT: Estructuramos el contenido para que Gemini distinga las variables
        prompt_estructurado = f"""
        NUEVO CORREO ENTRANTE PARA ANALIZAR:
        ----------------------------------
        REMITENTE_EMAIL: {remitente_correo}
        
        CUERPO_DEL_MENSAJE:
        {cuerpo_correo}
        ----------------------------------
        Por favor, extrae los datos necesarios y determina si se requiere invocar herramientas.
        """

        response = self.client.models.generate_content(
            model='gemini-3.5-flash-lite',
            contents=prompt_estructurado,
            config=self.config
        )
        
        ejecuciones = []
        
        # Evaluar si el ciclo del Run detectó la necesidad de usar herramientas (Function Calling)
        if response.function_calls:
            for call in response.function_calls:
                func_name = call.name
                func_args = call.args
                
                # Ejecutar la función correspondiente
                if func_name in self.available_tools:
                    resultado_tool = self.available_tools[func_name](**func_args)
                    ejecuciones.append({
                        "funcion": func_name,
                        "parametros_extraidos": func_args,
                        "resultado": resultado_tool
                    })
        
        return {
            "respuesta_analista": response.text if response.text else "Procesamiento de herramientas en ejecución.",
            "herramientas_invocadas": ejecuciones
        }
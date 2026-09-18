# UTP Assistant - Sistema de Automatización de Flujos
Propuesta técnica e implementación funcional para la Tarea Académica 2 (UTPConsult).

## Estructura del Proyecto
El proyecto está modularizado para cumplir con los estándares técnicos solicitados:
- `app.py`: Interfaz gráfica en Streamlit para simular la bandeja de entrada de correos.
- `src/agent/`: Configuración del modelo Gemini y carga del System Prompt.
- `src/tools/`: Implementación de Function Calling para Jira, Google Calendar y CRM.

## Instalación y Ejecución
1. Activa tu entorno virtual de Python.
2. Instala las dependencias: `pip install -r requirements.txt`
3. Configura tu API Key en el archivo `.env`.
4. Ejecuta el servidor: `streamlit run app.py`
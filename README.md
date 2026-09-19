# UTP Assistant - Sistema de Automatización de Flujos

Propuesta técnica e implementación funcional para la Tarea Académica 2 (UTPConsult).

## Estructura del Proyecto

El proyecto está modularizado para cumplir con los estándares técnicos solicitados:

- `app.py`: Interfaz gráfica en Streamlit para simular la bandeja de entrada de correos.
- `src/agent/`: Configuración del modelo Gemini y carga del System Prompt.
- `src/tools/`: Implementación de Function Calling para Jira, Google Calendar y CRM.

## Requisitos

- Python 3.10 o superior
- pip
- Cuenta de Google Cloud con acceso a Gemini
- Credenciales locales para Jira

## Instalación

1. Crear y activar un entorno virtual:
   ```bash
   python -m venv .venv
   .venv\Scripts\activate
   ```
2. Instalar dependencias:
   ```bash
   pip install -r requirements.txt
   ```
3. Copiar el archivo de ejemplo de entorno:
   ```bash
   copy .env.example .env
   ```
   o en Linux/macOS:
   ```bash
   cp .env.example .env
   ```
4. Completar tus credenciales reales en el archivo `.env`.
5. Ejecutar la app:
   ```bash
   streamlit run app.py
   ```

## Seguridad

- El archivo `.env` nunca debe subirse al repositorio.
- Los archivos `credentials.json`, `token.json` y cualquier secreto local quedan ignorados por Git.
- El archivo `.env.example` sí puede subirse porque sirve como plantilla para que el equipo configure sus credenciales.

## Variables de entorno esperadas

- `GEMINI_API_KEY`
- `JIRA_SERVER_URL`
- `JIRA_USER_EMAIL`
- `JIRA_API_TOKEN`
- `CRM_API_KEY`

## Equipo

Cada miembro debe usar su propia configuración local en el archivo `.env`, sin compartir secretos en GitHub.

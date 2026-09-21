import os
import base64
import datetime
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = ["https://www.googleapis.com/auth/calendar"]

def agendar_reunion_en_google_calendar(asunto: str, fecha_inicio: str, asistentes: list) -> dict:
    """
    Agenda una reunión de seguimiento técnico o comercial en el Google Calendar institucional.
    
    Args:
        asunto: Título o motivo de la reunión (ej: Discutir módulo de pagos).
        fecha_inicio: Fecha y hora en formato string o descripción textual relativa (ej: 'Próxima semana').
        asistentes: Lista con los nombres o correos de las personas que deben participar.
    """
    # RECONSTRUCCIÓN DINÁMICA PARA GITHUB CODESPACES
    creds_b64 = os.getenv("GOOGLE_CREDENTIALS_BASE64")
    token_b64 = os.getenv("GOOGLE_TOKEN_BASE64")

    # Si estamos en Codespaces y los archivos no existen físicamente, los creamos en memoria/disco temporal
    if creds_b64 and not os.path.exists("credentials.json"):
        with open("credentials.json", "wb") as f:
            f.write(base64.b64decode(creds_b64))
            
    if token_b64 and not os.path.exists("token.json"):
        with open("token.json", "wb") as f:
            f.write(base64.b64decode(token_b64))

    creds = None
    # Comprobar si ya existe una sesión guardada previamente
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
        
    # Si no hay credenciales válidas, iniciar el inicio de sesión automático
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not os.path.exists("credentials.json"):
                return {
                    "status": "error",
                    "herramienta": "Google Calendar API",
                    "msg": "Falta el archivo 'credentials.json' en la raíz."
                }
            # Carga el archivo de credenciales de escritorio limpio
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            
            # Abre un puerto dinámico libre en segundo plano
            creds = flow.run_local_server(port=0)
            
        # Guardar las credenciales para evitar loguearse en el futuro
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    try:
        # Inicializar el servicio oficial v3 de Google Calendar
        service = build("calendar", "v3", credentials=creds)
        
        # --- PARSEO Y CORRECCIÓN DEL RANGO TEMPORAL ---
        # Gemini suele enviar strings limpios con formato ISO como: "2026-09-22T15:00:00"
        # Nos aseguramos de limpiar cualquier sufijo para evitar desfases de UTC
        string_fecha = fecha_inicio.replace('Z', '').split('+')[0]
        
        dt_inicio = datetime.datetime.fromisoformat(string_fecha)
        # Forzamos que la reunión dure exactamente 1 hora en el futuro
        dt_fin = dt_inicio + datetime.timedelta(hours=1)
        
        # Google Calendar exige que los strings incluyan el offset u operación ISO estricta
        # Al no colocar zona horaria en el string, delegamos el control al parámetro 'timeZone'
        fecha_inicio_clean = dt_inicio.isoformat()
        fecha_fin_clean = dt_fin.isoformat()

        event_body = {
            'summary': asunto,
            'description': 'Reunión técnica automatizada por UTP Assistant.',
            'start': {
                'dateTime': fecha_inicio_clean,
                'timeZone': 'America/Lima',
            },
            'end': {
                'dateTime': fecha_fin_clean,
                'timeZone': 'America/Lima',
            },
            'attendees': [{'email': email.strip()} for email in asistentes if '@' in email],
        }

        # Ejecución e inserción real en la nube de Google
        evento_creado = service.events().insert(calendarId="primary", body=event_body).execute()
        
        return {
            "status": "success",
            "herramienta": "Google Calendar API (Producción Real)",
            "evento_id": evento_creado.get('id'),
            "msg": f"Reunión agendada de forma exitosa. Enlace: {evento_creado.get('htmlLink')}"
        }

    except Exception as e:
        return {
            "status": "error",
            "herramienta": "Google Calendar API",
            "msg": f"Fallo al insertar el evento: {str(e)}"
        }

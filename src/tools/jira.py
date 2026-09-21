import os
from jira import JIRA

def crear_ticket_en_jira(resumen: str, descripcion: str, prioridad: str = "Medium") -> dict:
    """
    Crea una nueva tarea o historia de usuario en el sistema Jira de UTPConsult basado en requisitos de software.
    
    Args:
        resumen: Título corto y directo que resume la necesidad del cliente.
        descripcion: Detalle completo de los requisitos extraídos del correo electrónico.
        prioridad: Nivel de urgencia de la tarea (Low, Medium, High). Por defecto es Medium.
    """
    try:
        # Cargar las credenciales reales de Jira desde el entorno seguro
        server_url = os.getenv("JIRA_SERVER_URL")
        user_email = os.getenv("JIRA_USER_EMAIL")
        api_token = os.getenv("JIRA_API_TOKEN")
        
        if not server_url or not user_email or not api_token:
            raise ValueError("Faltan configurar las credenciales de Jira en el archivo .env")

        # Inicializar el cliente oficial de Jira Cloud
        options = {'server': server_url}
        jira_client = JIRA(options, basic_auth=(user_email, api_token))
        
        # Mapear el texto de prioridad al id estándar que espera tu tablero de Jira
        # (Jira Cloud por defecto usa nombres idénticos: 'Low', 'Medium', 'High')
        priority_name = prioridad.capitalize() if prioridad.capitalize() in ["Low", "Medium", "High"] else "Medium"

        # Estructurar el cuerpo de la incidencia (Issue)
        issue_dict = {
            'project': 'UTP', # La Clave (Key) de 3 letras de tu espacio de trabajo
            'summary': resumen,
            'description': descripcion,
            'issuetype': {'name': 'Task'}, # 'Task' es el tipo por defecto en proyectos Kanban
            'priority': {'name': priority_name}
        }
        
        # Disparar la petición de inserción real a los servidores de Atlassian
        nuevo_ticket = jira_client.create_issue(fields=issue_dict)
        
        return {
            "status": "success",
            "herramienta": "Jira Service Desk (Producción Real)",
            "ticket_id": nuevo_ticket.key,  # Te devolverá dinámicamente UTP-1, UTP-2, etc.
            "resumen": resumen,
            "msg": "Ticket generado e insertado de forma exitosa en el tablero Kanban del equipo técnico."
        }
        
    except Exception as e:
        # Control de excepciones por si el token expiró o la URL es incorrecta
        return {
            "status": "error",
            "herramienta": "Jira Service Desk",
            "ticket_id": "ERROR-JIRA",
            "resumen": resumen,
            "msg": f"No se pudo completar la automatización. Detalles del fallo: {str(e)}"
        }
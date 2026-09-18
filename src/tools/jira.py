def crear_ticket_en_jira(resumen: str, descripcion: str, prioridad: str = "Medium") -> dict:
    """
    Crea una nueva tarea o historia de usuario en el sistema Jira de UTPConsult basado en requisitos de software.
    
    Args:
        resumen: Título corto y directo que resume la necesidad del cliente.
        descripcion: Detalle completo de los requisitos extraídos del correo electrónico.
        prioridad: Nivel de urgencia de la tarea (Low, Medium, High). Por defecto es Medium.
    """
    # Simulación de inserción en API corporativa de Jira
    return {
        "status": "success",
        "herramienta": "Jira Service Desk",
        "ticket_id": "UTP-502",
        "resumen": resumen,
        "msg": "Ticket generado exitosamente para el equipo de desarrollo técnico."
    }
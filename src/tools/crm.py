def actualizar_contacto_en_crm(nombre_cliente: str, empresa: str, correo_contacto: str = "No especificado") -> dict:
    """
    Registra o actualiza la ficha de un cliente potencial (lead) en la base de datos del CRM corporativo.
    
    Args:
        nombre_cliente: Nombre completo de la persona que envía el correo electrónico.
        empresa: Nombre de la organización o negocio al que representa el cliente.
        correo_contacto: Dirección electrónica del remitente para futuras comunicaciones.
    """
    # Simulación de inserción en API corporativa del CRM Hubspot/Salesforce
    return {
        "status": "success",
        "herramienta": "CRM UTPConsult",
        "lead_id": "CRM-7741",
        "cliente": nombre_cliente,
        "empresa": empresa,
        "msg": "Ficha de cliente prospecto registrada y sincronizada con éxito."
    }
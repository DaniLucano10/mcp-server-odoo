from mcp.types import TextContent
import json

def get_employees(odoo, limit=50):
    """
    Obtiene empleados con toda la información disponible.
    """
    employees = odoo.search_read(
        'hr.employee',
        domain=[],
        fields=[],  # <- vacío = todos los campos
        limit=limit
    )

    if not employees:
        return [TextContent(type="text", text=" **No hay empleados registrados**")]

    result = f" **{len(employees)} empleados encontrados:**\n\n"
    for e in employees:
        # mostramos cada empleado como JSON para ver toda la info
        result += json.dumps(e, indent=4, ensure_ascii=False)
        result += "\n\n" + ("-" * 50) + "\n\n"

    return [TextContent(type="text", text=result)]

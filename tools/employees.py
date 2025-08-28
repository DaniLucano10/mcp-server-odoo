from mcp.types import TextContent

def get_employees(odoo, limit=50):
    employees = odoo.search_read(
        'hr.employee',
        domain=[],
        fields=['name', 'job_title', 'private_email', 'work_phone', 'department_id', 'country_id'],
        limit=limit
    )

    if not employees:
        return [TextContent(type="text", text=" **No hay empleados registrados**")]

    result = f" **{len(employees)} empleados encontrados:**\n\n"
    for e in employees:
        result += f" **{e['name']}**\n"
        result += f"    Puesto: {e['job_title'] if e['job_title'] else 'N/A'}\n"
        result += f"    Email: {e['private_email'] if e['private_email'] else 'N/A'}\n"
        result += f"    Teléfono: {e['work_phone'] if e['work_phone'] else 'N/A'}\n"
        result += f"    Departamento: {e['department_id'][1] if e['department_id'] else 'N/A'}\n\n"
        result += f"    País: {e['country_id'][1] if e['country_id'] else 'N/A'}\n"

    return [TextContent(type="text", text=result)]

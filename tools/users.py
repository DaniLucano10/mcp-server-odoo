from mcp.types import TextContent

def get_users(odoo, limit=50):
    users = odoo.search_read(
        'res.users',
        domain=[],
        fields=['name', 'login', 'email', 'active'],
        limit=limit
    )

    if not users:
        return [TextContent(type="text", text=" **No hay usuarios registrados**")]

    result = f" **{len(users)} usuarios encontrados:**\n\n"
    for u in users:
        if not u.get('active', True):
            estado = " Inactivo"
        elif u.get('last_activity_time'):
            estado = f" Último acceso: {u['last_activity_time']}"
        else:
            estado = " Nunca se conectó"

        result += f" **{u['name']}**\n"
        result += f"    Usuario: {u['login']}\n"
        if u.get('email') and u['email'] != u['login']:
            result += f"    Email: {u['email']}\n"
        result += f"   {estado}\n\n"

    return [TextContent(type="text", text=result)]

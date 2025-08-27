from mcp.types import TextContent

def get_customers(odoo, limit=50):
    customers = odoo.search_read(
        'res.partner',
        domain=[['customer_rank', '>', 0]],
        fields=['name', 'email', 'phone', 'city'],
        limit=limit
    )
    if not customers:
        return [TextContent(type="text", text=" **No hay clientes registrados**")]

    result = f" **{len(customers)} clientes encontrados:**\n\n"
    for c in customers:
        result += f" **{c['name']}**\n"
        if c['email']: result += f"    {c['email']}\n"
        if c['phone']: result += f"   {c['phone']}\n"
        if c['city']: result += f"  {c['city']}\n\n"

    return [TextContent(type="text", text=result)]

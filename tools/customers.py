from mcp.types import TextContent
import json

def get_customers(odoo, limit=50):
    """
    Obtiene todos los clientes con toda la información disponible.
    """
    customers = odoo.search_read(
        'res.partner',
        domain=[['customer_rank', '>', 0]],  # Solo clientes
        fields=[],  
        limit=limit
    )

    if not customers:
        return [TextContent(type="text", text=" **No hay clientes registrados**")]

    result = f" **{len(customers)} clientes encontrados:**\n\n"
    for c in customers:
        # convertir cada registro en JSON legible
        result += json.dumps(c, indent=4, ensure_ascii=False)
        result += "\n\n" + ("-" * 50) + "\n\n"

    return [TextContent(type="text", text=result)]

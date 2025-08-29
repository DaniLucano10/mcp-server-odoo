from mcp.types import TextContent
import json

def get_purchases(odoo, limit=20):
    """
    Trae órdenes de compra con toda la información disponible.
    """
    # Obtener todos los campos del modelo purchase.order
    all_fields = list(odoo.fields_get('purchase.order').keys())

    purchases = odoo.search_read(
        'purchase.order',
        domain=[],
        fields=all_fields,
        limit=limit
    )

    if not purchases:
        return [TextContent(type="text", text=" **No hay órdenes de compra**")]

    result = f" **{len(purchases)} órdenes de compra encontradas:**\n\n"
    for p in purchases:
        result += json.dumps(p, indent=4, ensure_ascii=False)
        result += "\n\n" + ("-" * 50) + "\n\n"

    return [TextContent(type="text", text=result)]

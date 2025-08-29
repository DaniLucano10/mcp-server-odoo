from mcp.types import TextContent
import json

def get_stock(odoo, limit=50):
    """
    Obtiene niveles de stock con toda la información disponible.
    """
    # Obtener todos los campos del modelo stock.quant
    all_fields = list(odoo.fields_get('stock.quant').keys())

    stock = odoo.search_read(
        'stock.quant',
        domain=[],
        fields=all_fields,
        limit=limit
    )

    if not stock:
        return [TextContent(type="text", text=" **No hay stock disponible**")]

    result = f" **{len(stock)} registros de inventario encontrados:**\n\n"
    for s in stock:
        result += json.dumps(s, indent=4, ensure_ascii=False)
        result += "\n\n" + ("-" * 50) + "\n\n"

    return [TextContent(type="text", text=result)]

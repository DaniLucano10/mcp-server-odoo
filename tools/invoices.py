from mcp.types import TextContent
import json

def get_invoices(odoo, limit=20):
    """
    Obtiene facturas de clientes con toda la información disponible.
    """
    invoices = odoo.search_read(
        'account.move',
        domain=[['move_type', '=', 'out_invoice']],  # Solo facturas de clientes
        fields=[],  #  vacío = todos los campos
        limit=limit
    )

    if not invoices:
        return [TextContent(type="text", text=" **No hay facturas registradas**")]

    result = f" **{len(invoices)} facturas encontradas:**\n\n"
    for inv in invoices:
        # Lo convertimos a JSON con indentación para verlo más claro
        result += json.dumps(inv, indent=4, ensure_ascii=False)
        result += "\n\n" + ("-" * 50) + "\n\n"

    return [TextContent(type="text", text=result)]

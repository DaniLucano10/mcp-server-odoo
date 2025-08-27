from mcp.types import TextContent

def get_sale_orders(odoo, limit=20):
    orders = odoo.search_read(
        'sale.order',
        domain=[],
        fields=['name', 'partner_id', 'date_order', 'amount_total', 'state'],
        limit=limit
    )

    if not orders:
        return [TextContent(type="text", text=" **No hay órdenes de venta**")]

    result = f" **{len(orders)} órdenes encontradas:**\n\n"
    for o in orders:
        partner = o['partner_id'][1] if o['partner_id'] else "Cliente desconocido"
        result += f" **{o['name']}**\n"
        result += f"    Cliente: {partner}\n"
        result += f"    Fecha: {o['date_order']}\n"
        result += f"    Total: ${o['amount_total']}\n"
        result += f"    Estado: {o['state']}\n\n"

    return [TextContent(type="text", text=result)]

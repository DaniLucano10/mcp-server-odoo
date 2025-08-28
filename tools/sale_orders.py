from mcp.types import TextContent

def get_sale_orders(odoo, limit=20):
    fields_to_read = [
        'name',
        'partner_id',
        'date_order',
        'amount_total',
        'state',
        'activity_user_id',
        'amount_delivery',
        'amount_invoiced',
        'amount_paid',
        'amount_tax',
        'amount_to_invoice',
        'amount_untaxed',
        'commitment_date',
        'carrier_id',
        'client_order_ref',
        'delivery_count',
        'delivery_message'
    ]

    orders = odoo.search_read(
        'sale.order',
        domain=[],
        fields=fields_to_read,
        limit=limit
    )

    if not orders:
        return [TextContent(type="text", text=" **No hay órdenes de venta**")]

    result = f" **{len(orders)} órdenes encontradas:**\n\n"
    for o in orders:
        partner = o['partner_id'][1] if o['partner_id'] else "Cliente desconocido"
        user = o['activity_user_id'][1] if o.get('activity_user_id') else "Sin responsable"
        carrier = o['carrier_id'][1] if o.get('carrier_id') else "No asignado"

        result += f" **{o['name']}**\n"
        result += f"    Cliente: {partner}\n"
        result += f"    Usuario responsable: {user}\n"
        result += f"    Fecha de la orden: {o['date_order']}\n"
        result += f"    Fecha de entrega: {o.get('commitment_date', 'No definida')}\n"
        result += f"    Referencia cliente: {o.get('client_order_ref', '-')}\n"
        result += f"    Método de entrega: {carrier}\n"
        result += f"    Subtotal: ${o.get('amount_untaxed', 0)}\n"
        result += f"    Impuestos: ${o.get('amount_tax', 0)}\n"
        result += f"    Gastos de envío: ${o.get('amount_delivery', 0)}\n"
        result += f"    Total facturado: ${o.get('amount_invoiced', 0)}\n"
        result += f"    Total pagado: ${o.get('amount_paid', 0)}\n"
        result += f"    Total: ${o['amount_total']}\n"
        result += f"    Balance sin facturar: ${o.get('amount_to_invoice', 0)}\n"
        result += f"    Órdenes de entrega: {o.get('delivery_count', 0)}\n"
        result += f"    Mensaje de entrega: {o.get('delivery_message', '-')}\n"
        result += f"    Estado: {o['state']}\n\n"

    return [TextContent(type="text", text=result)]

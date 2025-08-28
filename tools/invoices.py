from mcp.types import TextContent

def get_invoices(odoo, limit=20):
    invoices = odoo.search_read(
        'account.move',
        domain=[['move_type', '=', 'out_invoice']],  # Solo facturas de clientes
        fields=['name', 'invoice_date', 'partner_id', 'amount_total', 'payment_state'],
        limit=limit
    )

    if not invoices:
        return [TextContent(type="text", text=" **No hay facturas registradas**")]

    result = f" **{len(invoices)} facturas encontradas:**\n\n"
    for inv in invoices:
        partner = inv['partner_id'][1] if inv['partner_id'] else "Cliente desconocido"
        result += f" **{inv['name']}**\n"
        result += f"    Cliente: {partner}\n"
        result += f"    Fecha: {inv['invoice_date']}\n"
        result += f"    Total: ${inv['amount_total']}\n"
        result += f"    Estado: {inv['payment_state']}\n\n"

    return [TextContent(type="text", text=result)]

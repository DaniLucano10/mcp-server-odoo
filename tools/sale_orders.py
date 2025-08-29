from mcp.types import TextContent

def _get_field_names(odoo, model='sale.order', limit=2000):
    """
    Obtiene todos los campos disponibles para el modelo,
    excluyendo binarios y campos sensibles/prohibidos.
    """
    try:
        recs = odoo.search_read(
            'ir.model.fields',
            domain=[('model', '=', model)],
            fields=['name', 'ttype'],
            limit=limit
        )
        skip_ttypes = {'binary'}
        skip_names_prefix = ('image', 'avatar')
        skip_forbidden = {'password', 'totp_secret', 'otp_secret'}

        names = []
        for r in recs:
            name = r.get('name')
            ttype = r.get('ttype')
            if not name:
                continue
            if ttype in skip_ttypes:
                continue
            if any(name.startswith(p) for p in skip_names_prefix):
                continue
            if name in skip_forbidden:
                continue
            names.append(name)

        return names

    except Exception:
        # fallback mínimo
        return ['name', 'partner_id', 'date_order', 'amount_total', 'state']


def get_sale_orders(odoo, limit=20, domain=None):
    """
    Trae órdenes de venta con todos los campos disponibles (menos binarios).
    """
    fields = _get_field_names(odoo, 'sale.order')
    orders = odoo.search_read(
        'sale.order',
        domain=domain or [],
        fields=fields,
        limit=limit
    )

    if not orders:
        return [TextContent(type="text", text=" **No hay órdenes de venta**")]

    result = f" **{len(orders)} órdenes encontradas:**\n\n"
    for o in orders:
        # Cabecera principal
        partner = o['partner_id'][1] if o.get('partner_id') else "Cliente desconocido"
        result += f" **{o.get('name','(sin nombre)')}**\n"
        result += f"    Cliente: {partner}\n"
        result += f"    Estado: {o.get('state','-')}\n"

        # Mostrar todos los campos
        for k, v in sorted(o.items()):
            if k in {'name', 'partner_id', 'state'}:
                continue  # ya mostrado arriba
            if isinstance(v, list) and len(v) == 2 and isinstance(v[0], int):
                # many2one
                result += f"   {k}: {v[1]} (ID {v[0]})\n"
            else:
                result += f"   {k}: {v}\n"

        result += "\n"

    return [TextContent(type="text", text=result)]

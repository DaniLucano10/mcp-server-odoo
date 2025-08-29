from mcp.types import TextContent

def _get_field_names(odoo, model='product.product', limit=2000):
    """
    Lee ir.model.fields para obtener todos los campos de un modelo,
    excluyendo binarios y campos sensibles.
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
        skip_forbidden = set()  # en productos no hay tantos prohibidos como en usuarios
        
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
        # fallback mínimo si algo falla
        return ['name', 'list_price', 'categ_id']


def get_products(odoo, limit=50, domain=None):
    # obtener dinámicamente todos los campos
    fields = _get_field_names(odoo, 'product.product')

    products = odoo.search_read(
        'product.product',
        domain=domain or [],
        fields=fields,
        limit=limit
    )

    if not products:
        return [TextContent(type="text", text=" **No hay productos registrados**")]

    result = f" **{len(products)} productos encontrados:**\n\n"
    for p in products:
        result += f" **{p.get('name','(sin nombre)')}**\n"
        # mostrar todos los campos
        for k, v in sorted(p.items()):
            if k == 'name':
                continue
            # si es relación Many2one → mostrar nombre
            if isinstance(v, list) and len(v) == 2 and isinstance(v[0], int):
                result += f"   {k}: {v[1]} (ID {v[0]})\n"
            else:
                result += f"   {k}: {v}\n"
        result += "\n"

    return [TextContent(type="text", text=result)]

from mcp.types import TextContent

def get_products(odoo, limit=50):
    products = odoo.search_read(
        'product.product',
        domain=[['sale_ok', '=', True]],
        fields=['name', 'compare_list_price', 'categ_id'],
        limit=limit
    )

    if not products:
        return [TextContent(type="text", text=" **No hay productos registrados**")]

    result = f" **{len(products)} productos encontrados:**\n\n"
    for p in products:
        result += f" **{p['name']}**\n"
        result += f"    ${p['compare_list_price']}\n"
        result += f"    Categoría: {p['categ_id'][1] if p['categ_id'] else 'N/A'}\n\n"

    return [TextContent(type="text", text=result)]

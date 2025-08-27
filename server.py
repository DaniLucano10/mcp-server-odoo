from mcp.server import Server
import mcp.types as types
from mcp.types import Tool
from tools.customers import get_customers
from tools.products import get_products
from tools.sale_orders import get_sale_orders
from tools.users import get_users

app = Server("odoo-mcp-final")

@app.list_tools()
async def handle_list_tools():
    return [
        Tool(name="get_customers", description="Obtener lista de clientes", inputSchema={"type":"object","properties":{"limit":{"type":"number","default":50}}}),
        Tool(name="get_products", description="Obtener lista de productos", inputSchema={"type":"object","properties":{"limit":{"type":"number","default":50}}}),
        Tool(name="get_sale_orders", description="Obtener órdenes de venta", inputSchema={"type":"object","properties":{"limit":{"type":"number","default":20}}}),
        Tool(name="get_users", description="Obtener lista de usuarios", inputSchema={"type":"object","properties":{"limit":{"type":"number","default":50}}}),
    ]

@app.call_tool()
async def handle_call_tool(name, arguments):
    from main import odoo  # evita import circular
    if not odoo:
        return [types.TextContent(type="text", text="No hay conexión con Odoo")]

    limit = arguments.get("limit")
    if name == "get_customers":
        return get_customers(odoo, limit)
    elif name == "get_products":
        return get_products(odoo, limit)
    elif name == "get_sale_orders":
        return get_sale_orders(odoo, limit)
    elif name == "get_users":
        return get_users(odoo, limit)
    else:
        return [types.TextContent(type="text", text=f"Herramienta '{name}' no encontrada")]

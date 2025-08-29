from mcp.server import Server
import mcp.types as types
from mcp.types import Tool
from tools.customers import get_customers
from tools.products import get_products
from tools.sale_orders import get_sale_orders
from tools.users import get_users
from tools.invoices import get_invoices
from tools.employees import get_employees

app = Server("odoo-mcp-final")

def set_odoo_connector(connector):
    global odoo
    odoo = connector

@app.list_tools()
async def handle_list_tools():
    return [
        Tool(name="get_customers", description="Obtener lista de clientes", inputSchema={"type":"object","properties":{"limit":{"type":"number","default":50}}}),
        Tool(name="get_products", description="Obtener lista de productos", inputSchema={"type":"object","properties":{"limit":{"type":"number","default":50}}}),
        Tool(name="get_sale_orders", description="Obtener órdenes de venta", inputSchema={"type":"object","properties":{"limit":{"type":"number","default":20}}}),
        Tool(name="get_users", description="Obtener lista de usuarios", inputSchema={"type":"object","properties":{"limit":{"type":"number","default":50}}}),
        Tool(name="get_invoices", description="Obtener lista de facturas", inputSchema={"type":"object","properties":{"limit":{"type":"number","default":20}}}),
        Tool(name="get_employees", description="Obtener lista de empleados", inputSchema={"type":"object","properties":{"limit":{"type":"number","default":50}}}),
        Tool(name="get_purchases", description="Obtener órdenes de compra", inputSchema={"type":"object","properties":{"limit":{"type":"number","default":20}}}),
        Tool(name="get_stock", description="Obtener niveles de stock", inputSchema={"type":"object","properties":{"limit":{"type":"number","default":50}}}),
    ]

@app.call_tool()
async def handle_call_tool(name, arguments):
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
    elif name == "get_invoices":
        return get_invoices(odoo, limit)
    elif name == "get_employees":
        return get_employees(odoo, limit)
    elif name == "get_purchases":
        return get_purchases(odoo, limit)
    elif name == "get_stock":
        return get_stock(odoo, limit)
    else:
        return [types.TextContent(type="text", text=f"Herramienta '{name}' no encontrada")]

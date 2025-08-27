#!/usr/bin/env python3
"""
Servidor MCP para Odoo - Versión definitiva compatible con Windows
"""

import asyncio
import os
import xmlrpc.client
from typing import Any, Dict, List
from dotenv import load_dotenv
import sys

# Importaciones MCP
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.server.models import InitializationOptions
import mcp.types as types
from mcp.types import Tool, TextContent

# ======================
# Conector Odoo
# ======================
class OdooConnector:
    """Conector para Odoo usando XML-RPC"""

    def __init__(self, url: str, db: str, username: str, password: str):
        self.url = url
        self.db = db
        self.username = username
        self.password = password
        self.uid = None
        self.models = None
        self.authenticate()

    def authenticate(self):
        """Autenticar con Odoo"""
        try:
            common = xmlrpc.client.ServerProxy(f'{self.url}/xmlrpc/2/common')
            self.uid = common.authenticate(self.db, self.username, self.password, {})
            if self.uid:
                self.models = xmlrpc.client.ServerProxy(f'{self.url}/xmlrpc/2/object')
                print(f"Conectado a Odoo como usuario ID: {self.uid}", file=sys.stderr)
            else:
                raise Exception("Falló la autenticación")
        except Exception as e:
            print(f"Error conectando con Odoo: {e}", file=sys.stderr)
            raise

    def search_read(self, model: str, domain: List = None, fields: List = None, limit: int = None):
        """Buscar y leer registros"""
        domain = domain or []
        fields = fields or []

        kwargs = {'fields': fields} if fields else {}
        if limit:
            kwargs['limit'] = limit

        return self.models.execute_kw(
            self.db, self.uid, self.password,
            model, 'search_read',
            [domain], kwargs
        )

# ======================
# Inicializar conexión Odoo
# ======================
odoo = None

def init_odoo_connection():
    """Inicializar conexión con Odoo"""
    global odoo
    load_dotenv()

    url = os.getenv('ODOO_URL')
    db = os.getenv('ODOO_DB')
    username = os.getenv('ODOO_USER')
    password = os.getenv('ODOO_PASSWORD')

    print(f"Conectando a: {url}", file=sys.stderr)
    print(f"Base de datos: {db}", file=sys.stderr)
    print(f"Usuario: {username}", file=sys.stderr)

    odoo = OdooConnector(url, db, username, password)

# ======================
# Servidor MCP
# ======================
app = Server("odoo-mcp-final")

@app.list_tools()
async def handle_list_tools() -> List[Tool]:
    """Lista de herramientas disponibles"""
    return [
        Tool(
            name="get_customers",
            description="Obtener lista de clientes de Odoo",
            inputSchema={"type": "object", "properties": {"limit": {"type": "number", "default": 50}}}
        ),
        Tool(
            name="get_products",
            description="Obtener lista de productos de Odoo",
            inputSchema={"type": "object", "properties": {"limit": {"type": "number", "default": 50}}}
        ),
        Tool(
            name="get_sale_orders",
            description="Obtener órdenes de venta de Odoo",
            inputSchema={"type": "object", "properties": {"limit": {"type": "number", "default": 20}}}
        ),
        Tool(
            name="get_users",
            description="Obtener lista de usuarios de Odoo",
            inputSchema={"type": "object", "properties": {"limit": {"type": "number", "default": 50}}}
        )
    ]

@app.call_tool()
async def handle_call_tool(name: str, arguments: Dict[str, Any]) -> List[TextContent]:
    """Manejar llamadas a herramientas"""
    if not odoo:
        return [TextContent(type="text", text="No hay conexión con Odoo")]

    try:
        if name == "get_customers":
            limit = arguments.get("limit", 50)
            customers = odoo.search_read(
                'res.partner',
                domain=[['customer_rank', '>', 0]],
                fields=['name', 'email', 'phone', 'city'],
                limit=limit
            )

            if customers:
                result = f" **{len(customers)} clientes encontrados:**\n\n"
                for c in customers:
                    result += f" **{c['name']}**\n"
                    if c['email']:
                        result += f"    {c['email']}\n"
                    if c['phone']:
                        result += f"   {c['phone']}\n"
                    if c['city']:
                        result += f"  {c['city']}\n"
                    result += "\n"
            else:
                result = " **No hay clientes registrados**\n\nPuedes agregar clientes desde Ventas → Clientes en Odoo."
            return [TextContent(type="text", text=result)]

        elif name == "get_products":
            limit = arguments.get("limit", 50)
            products = odoo.search_read(
                'product.product',
                domain=[['sale_ok', '=', True]],
                fields=['name', 'compare_list_price', 'categ_id'],
                limit=limit
            )

            if products:
                result = f" **{len(products)} productos encontrados:**\n\n"
                for p in products:
                    result += f" **{p['name']}**\n"
                    result += f"    ${p['compare_list_price']}\n"
                    result += f"    Stock: {p['categ_id']}\n\n"
            else:
                result = " **No hay productos registrados**\n\nPuedes agregar productos desde Ventas → Productos en Odoo."
            return [TextContent(type="text", text=result)]

        elif name == "get_sale_orders":
            limit = arguments.get("limit", 20)
            orders = odoo.search_read(
                'sale.order',
                domain=[],
                fields=['name', 'partner_id', 'date_order', 'amount_total', 'state'],
                limit=limit
            )

            if orders:
                result = f" **{len(orders)} órdenes encontradas:**\n\n"
                for o in orders:
                    result += f" **{o['name']}**\n"
                    result += f"    {o['partner_id'][1]}\n"
                    result += f"    {o['date_order']}\n"
                    result += f"    ${o['amount_total']}\n"
                    result += f"    {o['state']}\n\n"
            else:
                result = "**No hay órdenes de venta**\n\nLas órdenes aparecerán cuando se creen desde Ventas → Órdenes."
            return [TextContent(type="text", text=result)]

        elif name == "get_users":
            limit = arguments.get("limit", 50)
            users = odoo.search_read(
                'res.users',
                domain=[],
                fields=['name', 'login', 'email', 'active'],
                limit=limit
            )

            if users:
                result = f" **{len(users)} usuarios encontrados:**\n\n"
                for u in users:
                    # Determinar estado
                    if not u.get('active', True):
                        estado = " Inactivo"
                    elif u.get('last_activity_time'):
                        estado = f" Último acceso: {u['last_activity_time']}"
                    else:
                        estado = " Nunca se conectó"
                    
                    result += f" **{u['name']}**\n"
                    result += f"    {u['login']}\n"
                    if u['email'] and u['email'] != u['login']:
                        result += f"    Email: {u['email']}\n"
                    result += f"   {estado}\n\n"
            else:
                result = " **No hay usuarios registrados**"
            return [TextContent(type="text", text=result)]

        else:
            return [TextContent(type="text", text=f" Herramienta '{name}' no encontrada")]

    except Exception as e:
        return [TextContent(type="text", text=f" Error: {str(e)}")]

# ======================
# Función principal
# ======================
async def main():
    print("Iniciando servidor MCP para Odoo...", file=sys.stderr)
    try:
        init_odoo_connection()
        print(" Servidor MCP listo!", file=sys.stderr)

        async with stdio_server() as (read_stream, write_stream):
            await app.run(
                read_stream,
                write_stream,
                InitializationOptions(
                    server_name="odoo-mcp-server",
                    server_version="1.0.0",
                    capabilities=types.ServerCapabilities(
                        tools=types.ToolsCapability(listChanged=False),
                        resources=None,
                        prompts=None,
                        logging=None
                    )
                )
            )
    except asyncio.CancelledError:
        print("Servidor MCP cancelado", file=sys.stderr)
    except KeyboardInterrupt:
        print("Servidor MCP detenido por el usuario", file=sys.stderr)
    except Exception as e:
        print(f"Error del servidor: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()

# ======================
# Ejecución principal
# ======================
if __name__ == "__main__":
    try:
        print("=" * 60, file=sys.stderr)
        print(" SERVIDOR MCP ODOO - ITS Systems", file=sys.stderr)
        print("=" * 60, file=sys.stderr)
        asyncio.run(main())
    except KeyboardInterrupt:
        try:
            print("\n ¡Hasta luego!", file=sys.stderr)
        except ValueError:
            pass  # stdout cerrado
    except Exception as e:
        print(f"\n Error fatal: {e}", file=sys.stderr)
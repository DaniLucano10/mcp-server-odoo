import asyncio, sys
from mcp.server.stdio import stdio_server
import mcp.types as types
from mcp.server.models import InitializationOptions
from config import ODOO_URL, ODOO_DB, ODOO_USER, ODOO_PASSWORD
from odoo_connector import OdooConnector
from server import app

odoo = None

def init_odoo_connection():
    global odoo
    print(f"Conectando a: {ODOO_URL}", file=sys.stderr)
    odoo = OdooConnector(ODOO_URL, ODOO_DB, ODOO_USER, ODOO_PASSWORD)

async def main():
    print("Iniciando servidor MCP para Odoo...", file=sys.stderr)
    init_odoo_connection()
    async with stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream, write_stream,
            InitializationOptions(
                server_name="odoo-mcp-server",
                server_version="1.0.0",
                capabilities=types.ServerCapabilities(
                    tools=types.ToolsCapability(listChanged=False)
                )
            )
        )

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n ¡Hasta luego!", file=sys.stderr)

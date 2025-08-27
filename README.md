En C:\Users\ITS\AppData\Roaming\Claude o donde se haya instalado Claude crear el archivo claude_desktop_config.json:

{
    "mcpServers": {
        "odoo": {
            "command": "C:\\Users\\ITS\\Desktop\\Proy\\githubproyectos\\mcp-server-odoo\\venv\\Scripts\\python.exe",
            "args": ["C:\\Users\\ITS\\Desktop\\Proy\\githubproyectos\\mcp-server-odoo\\odoo_mcp_final.py"],
            "env": {
                "ODOO_URL": "https://midominio",
                "ODOO_DB": "mi_db",
                "ODOO_USER": "miusuario", 
                "ODOO_PASSWORD": "micontra"
            }
        }
    }
}

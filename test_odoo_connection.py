#!/usr/bin/env python3
"""
Script para probar la conexión con tu instancia de Odoo
Ejecuta este script primero para verificar que todo funcione
"""

import xmlrpc.client
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

def test_odoo_connection():
    """Probar conexión con Odoo usando tus credenciales"""
    
    # Obtener configuración del .env
    url = os.getenv('ODOO_URL')
    db = os.getenv('ODOO_DB') 
    username = os.getenv('ODOO_USER')
    password = os.getenv('ODOO_PASSWORD')
    
    print("🔧 Configuración cargada:")
    print(f"   URL: {url}")
    print(f"   Base de datos: {db}")
    print(f"   Usuario: {username}")
    
    if not password:
        print("   Contraseña:  NO CARGADA")
        print()
        print("   Error: No se pudieron cargar las variables de entorno")
        print("   Verifica que el archivo .env esté en el directorio actual")
        print("   Contenido esperado del .env:")
        print("   ODOO_URL=https://odoo-its.itscloud.store")
        print("   ODOO_DB=odoo_db")
        print("   ODOO_USER=admin@itsystems.pe")
        print("   ODOO_PASSWORD=YcCe6jX4G6QTrOg5e75M")
        return False
    else:
        print(f"   Contraseña: {'*' * len(password)}")
    print()
    
    try:
        print("🔗 Intentando conectar con Odoo...")
        
        # Conectar con el servicio común
        common = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/common')
        
        # Obtener versión de Odoo
        version = common.version()
        print(f" Conexión exitosa!")
        print(f"   Versión Odoo: {version['server_version']}")
        print(f"   Serie: {version['server_serie']}")
        print()
        
        # Autenticar usuario
        print("Autenticando usuario...")
        uid = common.authenticate(db, username, password, {})
        
        if uid:
            print(f"Usuario autenticado exitosamente!")
            print(f"   ID de usuario: {uid}")
            print()
            
            # Probar acceso a modelos
            print("📋 Probando acceso a datos...")
            models = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/object')
            
            # Contar clientes
            customer_count = models.execute_kw(
                db, uid, password,
                'res.partner', 'search_count',
                [[['customer_rank', '>', 0]]]
            )
            print(f" Clientes encontrados: {customer_count}")
            
            # Contar productos
            product_count = models.execute_kw(
                db, uid, password,
                'product.product', 'search_count',
                [[['sale_ok', '=', True]]]
            )
            print(f"Productos encontrados: {product_count}")
            
            # Contar órdenes de venta
            order_count = models.execute_kw(
                db, uid, password,
                'sale.order', 'search_count',
                [[]]
            )
            print(f"Órdenes de venta: {order_count}")
            
            print()
            print("¡Conexión completamente funcional!")
            print("   Ya puedes usar el servidor MCP con Claude.")
            
            return True
            
        else:
            print("Error: Falló la autenticación")
            print("   Verifica usuario y contraseña")
            return False
            
    except xmlrpc.client.Fault as e:
        print(f"Error XML-RPC: {e}")
        return False
    except Exception as e:
        print(f"Error de conexión: {e}")
        print("   Verifica la URL y conectividad de red")
        return False

if __name__ == "__main__":
    print("Probando conexión con Odoo ITS Systems")
    print("=" * 50)
    
    success = test_odoo_connection()
    
    print("=" * 50)
    if success:
        print("Todo listo para usar con Claude!")
    else:
        print("Revisa la configuración antes de continuar")
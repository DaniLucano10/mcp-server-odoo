import xmlrpc.client
import sys

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

    def search_read(self, model: str, domain=None, fields=None, limit=None):
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

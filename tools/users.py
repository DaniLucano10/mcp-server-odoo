from mcp.types import TextContent

def _get_field_names(odoo, model='res.users', limit=2000):
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
        skip_forbidden = {'totp_secret', 'password', 'otp_secret'}
        
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

        # Solo añadimos campos clave SI existen en la base
        available = set(names)
        for must in ('name', 'login', 'email', 'active',
                     'last_login', 'last_activity_time', 'login_date'):
            if must in available and must not in names:
                names.append(must)

        return names

    except Exception:
        # fallback mínimo si no se puede leer ir.model.fields
        return ['name', 'login', 'email', 'active', 'last_activity_time', 'login_date']


def get_users(odoo, limit=50, domain=None):
    fields = _get_field_names(odoo, 'res.users')
    users = odoo.search_read(
        'res.users',
        domain=domain or [],
        fields=fields,
        limit=limit
    )

    if not users:
        return [TextContent(type="text", text=" **No hay usuarios registrados**")]

    result = f" **{len(users)} usuarios encontrados:**\n\n"
    for u in users:
        # Estado del usuario → elegimos el campo que exista
        if not u.get('active', True):
            estado = " Inactivo"
        elif 'last_login' in u and u['last_login']:
            estado = f" Último acceso: {u['last_login']}"
        elif 'last_activity_time' in u and u['last_activity_time']:
            estado = f" Última actividad: {u['last_activity_time']}"
        elif 'login_date' in u and u['login_date']:
            estado = f" Último login: {u['login_date']}"
        else:
            estado = " Nunca se conectó"

        # Cabecera del usuario
        result += f" **{u.get('name','(sin nombre)')}**\n"
        result += f"    Usuario: {u.get('login','-')}\n"
        if u.get('email') and u['email'] != u.get('login'):
            result += f"    Email: {u['email']}\n"
        result += f"   {estado}\n"

        # Mostrar todos los demás campos
        for k, v in sorted(u.items()):
            if k in {'name', 'login', 'email', 'active',
                     'last_login', 'last_activity_time', 'login_date'}:
                continue
            if isinstance(v, list) and len(v) == 2 and isinstance(v[0], int):
                result += f"   {k}: {v[1]} (ID {v[0]})\n"
            else:
                result += f"   {k}: {v}\n"

        result += "\n"

    return [TextContent(type="text", text=result)]


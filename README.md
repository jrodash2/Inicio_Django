# Portal Usuarios (Django)

Proyecto base en Django 5.x para gestionar usuarios, perfiles y permisos por grupos.

## Requisitos
- Python 3.12+
- Pip y virtualenv (opcional pero recomendado)
- Dependencias del proyecto: `pip install "django>=5,<6"`

## Puesta en marcha rápida
1. Crear y activar un entorno virtual (opcional):
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Windows: .venv\Scripts\activate
   ```
2. Instalar dependencias:
   ```bash
   pip install "django>=5,<6" Pillow
   ```
3. Aplicar migraciones iniciales (esto crea las tablas de sesiones, perfiles y evita errores como `no such table: django_session`):
   ```bash
   python manage.py migrate
   ```
4. Crear grupos y usuarios iniciales (jrodas y rodas) según los permisos solicitados:
   ```bash
   python manage.py setup_portal
   # o, si prefieres un nombre en español:
   python manage.py crear_grupos_y_usuarios
   ```
5. Iniciar el servidor de desarrollo:
   ```bash
   python manage.py runserver
   ```
6. Acceder a `http://127.0.0.1:8000/` e iniciar sesión con:
   - Usuario: `jrodas` / Contraseña: `99998888` (superusuario, grupo administrador)
   - Usuario: `rodas` / Contraseña: `99998888` (grupo gestor)

## Notas
- Si necesitas recrear la base de datos, elimina `db.sqlite3` y repite los pasos de migración y creación de usuarios.
- Las zonas horarias y localización están configuradas a `America/Guatemala` y español.

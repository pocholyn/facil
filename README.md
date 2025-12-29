# FACil - Sistema de Facturación

Sistema de gestión de facturación desarrollado con Django.

## Características

- Gestión de clientes, actividades y planes
- Creación y gestión de ofertas
- Conversión de ofertas a facturas
- Generación de PDFs
- Panel de administración completo

## Instalación

1. Clona el repositorio:
```bash
git clone https://github.com/tu-usuario/facil.git
cd facil
```

2. Crea un entorno virtual:
```bash
python -m venv .venv
source .venv/bin/activate  # En Windows: .venv\Scripts\activate
```

3. Instala las dependencias:
```bash
pip install -r requirements.txt
```

4. Configura las variables de entorno:
```bash
cp .env.example .env
# Edita .env con tus configuraciones
```

5. Ejecuta las migraciones:
```bash
python manage.py migrate
```

6. Crea un superusuario:
```bash
python manage.py createsuperuser
```

7. Ejecuta el servidor:
```bash
python manage.py runserver
```

## Despliegue en Railway

1. Sube el código a GitHub
2. Conecta tu repositorio a Railway
3. Railway detectará automáticamente la configuración de Django
4. Configura las variables de entorno en Railway:
   - `SECRET_KEY`: Genera una nueva clave secreta
   - `DEBUG`: False
   - `ALLOWED_HOSTS`: Tu dominio de Railway
   - `DATABASE_URL`: Se configura automáticamente por Railway

## Tecnologías utilizadas

- Django 4.2
- PostgreSQL
- Bootstrap 5
- Gunicorn
- WhiteNoise

## Licencia

Este proyecto está bajo la Licencia MIT.
# Guía de Despliegue - Sistema FACil

Esta guía detalla los pasos necesarios para desplegar el sistema FACil en un servidor Debian.

## Índice
1. [Requisitos del Sistema](#requisitos-del-sistema)
2. [Instalación de Dependencias](#instalación-de-dependencias)
3. [Configuración del Entorno](#configuración-del-entorno)
4. [Configuración de la Base de Datos](#configuración-de-la-base-de-datos)
5. [Configuración del Servidor Web](#configuración-del-servidor-web)
6. [Despliegue de la Aplicación](#despliegue-de-la-aplicación)
7. [Configuración de SSL](#configuración-de-ssl)
8. [Mantenimiento](#mantenimiento)

## Requisitos del Sistema

### Hardware Recomendado
- CPU: 2 cores o más
- RAM: 4GB mínimo
- Almacenamiento: 20GB mínimo

### Software Base
- Debian 11 o superior
- Python 3.8 o superior
- PostgreSQL 13 o superior
- Nginx
- Certbot (para SSL)

## Instalación de Dependencias

### Actualizar el Sistema
```bash
sudo apt update
sudo apt upgrade -y
```

### Instalar Paquetes del Sistema
```bash
sudo apt install -y python3-pip python3-venv postgresql postgresql-contrib nginx git certbot python3-certbot-nginx
```

### Crear Usuario de la Aplicación
```bash
sudo useradd -m -s /bin/bash facil
sudo usermod -aG sudo facil
```

## Configuración del Entorno

### Clonar el Repositorio
```bash
cd /opt
sudo git clone [URL_DEL_REPOSITORIO] facil
sudo chown -R facil:facil facil
```

### Crear Entorno Virtual
```bash
cd /opt/facil
python3 -m venv venv
source venv/bin/activate
```

### Instalar Dependencias Python
```bash
pip install -r requirements.txt
pip install gunicorn psycopg2-binary
```

## Configuración de la Base de Datos

### Crear Base de Datos y Usuario
```sql
sudo -u postgres psql

CREATE DATABASE facil;
CREATE USER facil_user WITH PASSWORD 'tu_contraseña_segura';
ALTER ROLE facil_user SET client_encoding TO 'utf8';
ALTER ROLE facil_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE facil_user SET timezone TO 'America/Havana';
GRANT ALL PRIVILEGES ON DATABASE facil TO facil_user;
\q
```

### Configurar Django para PostgreSQL
Modificar `facturacion/settings.py`:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'facil',
        'USER': 'facil_user',
        'PASSWORD': 'tu_contraseña_segura',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

# Configuraciones de producción
DEBUG = False
ALLOWED_HOSTS = ['tu_dominio.com', 'www.tu_dominio.com']

# Configuración de archivos estáticos y media
STATIC_ROOT = '/opt/facil/static/'
MEDIA_ROOT = '/opt/facil/media/'
```

### Migrar la Base de Datos
```bash
python manage.py migrate
python manage.py collectstatic
```

## Configuración del Servidor Web

### Configurar Gunicorn
Crear `/etc/systemd/system/gunicorn_facil.service`:
```ini
[Unit]
Description=gunicorn daemon para FACil
After=network.target

[Service]
User=facil
Group=www-data
WorkingDirectory=/opt/facil
ExecStart=/opt/facil/venv/bin/gunicorn --access-logfile - --workers 3 --bind unix:/opt/facil/facil.sock facturacion.wsgi:application

[Install]
WantedBy=multi-user.target
```

### Configurar Nginx
Crear `/etc/nginx/sites-available/facil`:
```nginx
server {
    listen 80;
    server_name tu_dominio.com www.tu_dominio.com;

    location = /favicon.ico { access_log off; log_not_found off; }
    
    location /static/ {
        root /opt/facil;
    }

    location /media/ {
        root /opt/facil;
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/opt/facil/facil.sock;
    }
}
```

### Activar el Sitio
```bash
sudo ln -s /etc/nginx/sites-available/facil /etc/nginx/sites-enabled
sudo nginx -t
sudo systemctl restart nginx
```

## Configuración de SSL

### Obtener Certificado SSL
```bash
sudo certbot --nginx -d tu_dominio.com -d www.tu_dominio.com
```

## Mantenimiento

### Respaldos de Base de Datos
Crear script `/opt/facil/backup.sh`:
```bash
#!/bin/bash
BACKUP_DIR="/opt/facil/backups"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
DATABASE="facil"

# Crear directorio de respaldo si no existe
mkdir -p $BACKUP_DIR

# Realizar respaldo
pg_dump -U facil_user $DATABASE > $BACKUP_DIR/backup_$TIMESTAMP.sql

# Mantener solo los últimos 7 respaldos
find $BACKUP_DIR -name "backup_*.sql" -mtime +7 -delete
```

### Actualización del Sistema
```bash
# Activar entorno virtual
source /opt/facil/venv/bin/activate

# Detener servicios
sudo systemctl stop gunicorn_facil

# Actualizar código
git pull origin main

# Instalar dependencias
pip install -r requirements.txt

# Migraciones
python manage.py migrate
python manage.py collectstatic --noinput

# Reiniciar servicios
sudo systemctl start gunicorn_facil
sudo systemctl restart nginx
```

### Monitoreo
Se recomienda configurar:
- Monitoreo de logs con `logrotate`
- Supervisión del sistema con `monit` o similar
- Alertas de espacio en disco y uso de recursos

### Permisos y Seguridad
```bash
# Asegurar permisos correctos
sudo chown -R facil:www-data /opt/facil
sudo chmod -R 755 /opt/facil
sudo chmod -R 770 /opt/facil/media

# Configurar firewall
sudo ufw allow 80
sudo ufw allow 443
sudo ufw allow 22
```

## Troubleshooting

### Logs Importantes
- Nginx: `/var/log/nginx/error.log`
- Gunicorn: `/var/log/gunicorn/error.log`
- Django: `/opt/facil/logs/django.log`

### Comandos Útiles
```bash
# Ver estado de servicios
sudo systemctl status gunicorn_facil
sudo systemctl status nginx

# Ver logs en tiempo real
sudo tail -f /var/log/nginx/error.log

# Verificar configuración de nginx
sudo nginx -t
```

## Notas Adicionales

### Optimización de Rendimiento
1. Configurar caché de Django
2. Optimizar consultas a la base de datos
3. Configurar compresión gzip en Nginx
4. Implementar CDN para archivos estáticos

### Seguridad
1. Mantener el sistema actualizado
2. Configurar copias de seguridad automáticas
3. Implementar monitoreo de seguridad
4. Mantener políticas de contraseñas fuertes
5. Configurar fail2ban para protección contra ataques

### Mantenimiento Regular
1. Revisar logs regularmente
2. Monitorear uso de recursos
3. Realizar copias de seguridad
4. Actualizar dependencias
5. Revisar certificados SSL
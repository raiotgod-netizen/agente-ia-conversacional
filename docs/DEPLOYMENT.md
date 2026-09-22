# Deployment Guide

## Opciones de deployment

El AI Agent Kit puede desplegarse de varias maneras segun tus necesidades.

## 1. Local (Desarrollo)

La forma mas simple de ejecutar el proyecto.

### Requisitos

- Python 3.10+
- pip

### Pasos

```bash
# Clonar repositorio
git clone https://github.com/TU_USUARIO/ai-agent-kit.git
cd ai-agent-kit

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar gateway (Terminal 1)
python gateway/server.py

# Ejecutar webui (Terminal 2)
python webui/server.py
```

### Verificacion

```bash
# Verificar gateway
curl http://localhost:8642/health

# Verificar webui
curl http://localhost:8787
```

## 2. Windows Service

Ejecutar como servicio de Windows que inicia automaticamente.

### Crear script de inicio

Crear archivo `start_services.bat`:

```batch
@echo off
start "AI Agent Gateway" python gateway/server.py
timeout /t 2
start "AI Agent WebUI" python webui/server.py
echo Servicios iniciados
pause
```

### Agregar a inicio automatico

1. Presiona `Win + R`
2. Escribe `shell:startup`
3. Crea un acceso directo de `start_services.bat`
4. Reinicia el PC

### Usar nssm (servicio nativo)

```bash
# Descargar nssm desde https://nssm.cc
# Instalar gateway como servicio
nssm install "AI Agent Gateway" python gateway/server.py
nssm install "AI Agent WebUI" python webui/server.py

# Iniciar servicios
nssm start "AI Agent Gateway"
nssm start "AI Agent WebUI"
```

## 3. Docker

Desplegar en containers para aislamiento y portabilidad.

### Dockerfile

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copiar archivos
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY gateway/ gateway/
COPY webui/ webui/

# Puertos
EXPOSE 8642 8787

# Comando por defecto
CMD ["sh", "-c", "python gateway/server.py & python webui/server.py"]
```

### docker-compose.yml

```yaml
version: '3.8'

services:
  gateway:
    build: .
    ports:
      - "8642:8642"
    volumes:
      - ./gateway/config.json:/app/gateway/config.json
      - ./data:/app/data
    environment:
      - OLLAMA_URL=http://host.docker.internal:11434
    restart: unless-stopped

  webui:
    build: .
    command: python webui/server.py
    ports:
      - "8787:8787"
    depends_on:
      - gateway
    restart: unless-stopped
```

### Comandos Docker

```bash
# Build y ejecutar
docker-compose up -d

# Ver logs
docker-compose logs -f

# Detener
docker-compose down

# Reconstruir
docker-compose up -d --build
```

## 4. Linux (Systemd)

Desplegar como servicio en Linux con systemd.

### Crear archivo de servicio

Crear `/etc/systemd/system/ai-agent.service`:

```ini
[Unit]
Description=AI Agent Gateway
After=network.target

[Service]
Type=simple
User=usuario
WorkingDirectory=/home/usuario/ai-agent-kit
ExecStart=/usr/bin/python3 gateway/server.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

### Activar servicio

```bash
# Recargar systemd
sudo systemctl daemon-reload

# Habilitar inicio automatico
sudo systemctl enable ai-agent

# Iniciar servicio
sudo systemctl start ai-agent

# Ver estado
sudo systemctl status ai-agent

# Ver logs
sudo journalctl -u ai-agent -f
```

## 5. VPS (Servidor Virtual)

Desplegar en un VPS para acceso remoto.

### Configuracion del servidor

```bash
# Actualizar sistema
sudo apt update && sudo apt upgrade -y

# Instalar Python
sudo apt install python3 python3-pip -y

# Instalar dependencias del sistema
sudo apt install -y gcc libffi-dev

# Clonar repositorio
cd /home/usuario
git clone https://github.com/TU_USUARIO/ai-agent-kit.git
cd ai-agent-kit

# Instalar dependencias
pip3 install -r requirements.txt

# Configurar
cp gateway/config.example.json gateway/config.json
nano gateway/config.json  # Editar configuracion
```

### Configurar firewall

```bash
# Abrir puertos
sudo ufw allow 8642/tcp
sudo ufw allow 8787/tcp
sudo ufw enable

# Verificar
sudo ufw status
```

### Ejecutar con screen

```bash
# Crear sesion para gateway
screen -S gateway
python3 gateway/server.py
# Presionar Ctrl+A, luego D para detach

# Crear sesion para webui
screen -S webui
python3 webui/server.py
# Presionar Ctrl+A, luego D para detach

# Ver sesiones
screen -ls

# Reconectar
screen -r gateway
screen -r webui
```

### Ejecutar con tmux

```bash
# Crear sesion
tmux new-session -d -s ai-agent

# Dividir paneles
tmux split-window -h
tmux send-keys "python3 gateway/server.py" C-m
tmux select-pane -t 0
tmux send-keys "python3 webui/server.py" C-m

# Adjuntar
tmux attach-session -t ai-agent
```

## 6. Cloud (AWS/GCP/Azure)

Desplegar en la nube para escalabilidad.

### AWS EC2

1. Crear instancia t2.micro (gratuita)
2. Conectar via SSH
3. Instalar Python y dependencias
4. Clonar repositorio
5. Configurar security group (puertos 8642, 8787)
6. Ejecutar con screen/tmux

### Google Cloud Run

```yaml
# app.yaml
runtime: python311
entrypoint: python gateway/server.py

instance_class: F1

env_variables:
  PROVIDER: "groq"
  API_KEY: "gsk_tu-key"
  MODEL: "llama-3.1-8b-instant"

automatic_scaling:
  min_instances: 0
  max_instances: 2
```

### Azure App Service

```json
// .deployment
{
  "settings": {
    "SCM_DO_BUILD_DURING_DEPLOYMENT": "true"
  }
}
```

## 7. Raspberry Pi

Desplegar en Raspberry Pi para un servidor casero.

### Configuracion

```bash
# Actualizar sistema
sudo apt update && sudo apt upgrade -y

# Instalar Python
sudo apt install python3 python3-pip -y

# Instalar dependencias
pip3 install requests duckduckgo-search

# Clonar y configurar
git clone https://github.com/TU_USUARIO/ai-agent-kit.git
cd ai-agent-kit
pip3 install -r requirements.txt

# Configurar para Pi
nano gateway/config.json
```

### Configuracion para Pi

```json
{
    "provider": "ollama",
    "model": "qwen3:4b",
    "ollama_url": "http://localhost:11434",
    "max_tokens": 300,
    "temperature": 0.7
}
```

### Ejecutar

```bash
# Usar screen
screen -S ai-agent
python3 gateway/server.py
```

## Seguridad en produccion

### HTTPS con Let's Encrypt

```bash
# Instalar certbot
sudo apt install certbot -y

# Obtener certificado
sudo certbot certonly --standalone -d tu-dominio.com

# Configurar nginx
sudo nano /etc/nginx/sites-available/ai-agent
```

### Configuracion nginx

```nginx
server {
    listen 443 ssl;
    server_name tu-dominio.com;

    ssl_certificate /etc/letsencrypt/live/tu-dominio.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/tu-dominio.com/privkey.pem;

    location / {
        proxy_pass http://localhost:8787;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }

    location /api/ {
        proxy_pass http://localhost:8642/;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }
}
```

### Rate limiting con nginx

```nginx
http {
    limit_req_zone $binary_remote_addr zone=ai:10m rate=10r/s;

    server {
        location /api/ {
            limit_req zone=ai burst=20 nodelay;
            proxy_pass http://localhost:8642/;
        }
    }
}
```

## Monitoreo

### Health check

```bash
# Script de health check
#!/bin/bash
if ! curl -s http://localhost:8642/health > /dev/null; then
    echo "Gateway down, reiniciando..."
    systemctl restart ai-agent-gateway
fi
```

### Cron de health check

```bash
# Agregar cron
crontab -e

# Ejecutar cada 5 minutos
*/5 * * * * /home/usuario/health_check.sh
```

### Logging

```python
# En gateway/server.py
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/var/log/ai-agent.log'),
        logging.StreamHandler()
    ]
)
```

## Backup

### Backup de configuracion

```bash
#!/bin/bash
BACKUP_DIR="/home/usuario/backups/ai-agent"
DATE=$(date +%Y%m%d_%H%M%S)

mkdir -p $BACKUP_DIR
cp -r /home/usuario/ai-agent-kit/gateway/config.json $BACKUP_DIR/config_$DATE.json
cp -r /home/usuario/ai-agent-kit/gateway/memory.json $BACKUP_DIR/memory_$DATE.json

# Mantener solo ultimos 7 backups
ls -t $BACKUP_DIR/config_*.json | tail -n +8 | xargs rm -f
ls -t $BACKUP_DIR/memory_*.json | tail -n +8 | xargs rm -f
```

### Cron de backup

```bash
# Ejecutar diariamente a las 3 AM
0 3 * * * /home/usuario/backup_ai_agent.sh
```

## Escalamiento horizontal

### Multiples instancias

```python
# nginx.conf
upstream ai_agent {
    server localhost:8642;
    server localhost:8643;
    server localhost:8644;
}

server {
    location /api/ {
        proxy_pass http://ai_agent;
    }
}
```

### Load balancer

```python
# gateway/server.py
import random

GATEWAYS = [
    {"host": "127.0.0.1", "port": 8642},
    {"host": "127.0.0.1", "port": 8643},
    {"host": "127.0.0.1", "port": 8644},
]

def get_gateway():
    return random.choice(GATEWAYS)
```

## Troubleshooting

### "Puerto en uso"

```bash
# Encontrar proceso usando el puerto
lsof -i :8642
# o
netstat -tulpn | grep 8642

# Matar el proceso
kill -9 <PID>
```

### "Permiso denegado"

```bash
# Cambiar permisos
chmod +x gateway/server.py
chmod +x webui/server.py

# O ejecutar con python
python3 gateway/server.py
```

### "No se encuentra python"

```bash
# Verificar instalacion
which python3
python3 --version

# Si no esta, instalar
sudo apt install python3 python3-pip -y
```

### "Error de conexion a base de datos"

```bash
# Verificar permisos del archivo
ls -la gateway/memory.db

# Si no existe, crear
touch gateway/memory.db
chmod 644 gateway/memory.db
```

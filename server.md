Я помогу вам развернуть проект Legal Neural Assistant в директории `/root/legalneuralassistant1`. Вот детализированная инструкция:

### 1. Подготовка директории

```bash
# Переход в директорию
cd /root/legalneuralassistant1
```

### 2. Установка зависимостей системы

```bash
# Обновление системы
apt update && apt upgrade -y

# Установка необходимых пакетов
    apt install -y python3-pip python3-venv python3-dev nginx git
```

### 3. Создание виртуального окружения

```bash
# Создание виртуального окружения
python3 -m venv venv

# Активация виртуального окружения
source venv/bin/activate
```

### 4. Установка зависимостей проекта

```bash
# Установка зависимостей из requirements.txt
pip install -r requirements.txt
```

### 5. Настройка .env файла

```bash
# Создание .env файла
nano .env

# Примерное содержимое:
SECRET_KEY=ваш_секретный_ключ_django
DEBUG=False
DJANGO_SETTINGS_MODULE=legal_assistant.settings
OPENAI_API_KEY=ваш_openai_api_ключ
```


### 6. Настройка базы данных

```bash
# Выполнение миграций
python manage.py makemigrations
python manage.py migrate

# Создание суперпользователя
python manage.py createsuperuser
```

### 7. Сбор статических файлов

```bash
python manage.py collectstatic
```

### 8. Установка и настройка Gunicorn

```bash
# Установка Gunicorn
pip install gunicorn

# Создание systemd службы
nano /etc/systemd/system/legalassistant.service

# Содержимое службы:
[Unit]
Description=Gunicorn instance to serve Legal Assistant Django App
After=network.target

[Service]
User=root
Group=root
WorkingDirectory=/root/legalneuralassistant1/legal_assistant
ExecStart=/root/legalneuralassistant1/venv/bin/gunicorn --workers 3 --bind 127.0.0.1:8000 legal_assistant.wsgi:application
Environment="PATH=/root/legalneuralassistant1/venv/bin"
Environment="PYTHONPATH=/root/legalneuralassistant1/legal_assistant"

[Install]
WantedBy=multi-user.target

# Запуск и активация службы
systemctl start legalassistant
systemctl enable legalassistant
```
```bash
 Перезагрузите systemd:
После внесения изменений выполните команды:
systemctl daemon-reload
systemctl restart legalassistant

4. Проверьте статус сервиса:
bash
Копировать код
systemctl status legalassistant

```bash


```bash

### 9. Настройка Nginx

```bash
Установите Nginx, если он еще не установлен:
apt install nginx -y

Проверьте статус Nginx:
systemctl status nginx

# Создание конфигурации Nginx
nano /etc/nginx/sites-available/legalneuralassistant

# Содержимое конфигурации:
server {
    listen 80;
    server_name legalneura.ddns.net;

    root /root/legalneuralassistant1;
    index index.html index.htm;

    location / {
        proxy_pass http://127.0.0.1:8000; # Убедитесь, что приложение работает на этом порту
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # Обработка ошибок
    error_page 404 /404.html;
    location = /404.html {
        internal;
    }
}


# Создание символической ссылки
ln -s /etc/nginx/sites-available/legalneuralassistant /etc/nginx/sites-enabled/

# Проверка конфигурации Nginx
nginx -t

# Перезапуск Nginx
systemctl restart nginx
```
```bash
Дополнительные настройки безопасности
Настройка SSL с помощью Let's Encrypt (по желанию) Для обеспечения безопасности можно настроить SSL-сертификат через Let's Encrypt:

apt install certbot python3-certbot-nginx
certbot --nginx -d legalneura.ddns.net

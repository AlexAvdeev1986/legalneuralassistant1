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
nano /etc/systemd/system/legal_assistant.service

# Содержимое службы:
[Unit]
Description=Legal Neural Assistant Gunicorn Daemon
After=network.target

[Service]
User=root
Group=root
WorkingDirectory=/root/legalneuralassistant1
ExecStart=/root/legalneuralassistant1/venv/bin/gunicorn \
          --workers 3 \
          --bind unix:/root/legalneuralassistant1/legal_assistant.sock \
          legal_assistant.wsgi:application

[Install]
WantedBy=multi-user.target

# Запуск и активация службы
systemctl start legal_assistant
systemctl enable legal_assistant
```

### 9. Настройка Nginx

```bash
# Создание конфигурации Nginx
nano /etc/nginx/sites-available/legal_assistant

# Содержимое конфигурации:
server {
    listen 80;
    server_name ваш_домен_или_ip;

    location = /favicon.ico { access_log off; log_not_found off; }
    
    location /static/ {
        root /root/legalneuralassistant1;
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/root/legalneuralassistant1/legal_assistant.sock;
    }
}

# Создание символической ссылки
ln -s /etc/nginx/sites-available/legal_assistant /etc/nginx/sites-enabled/

# Проверка конфигурации Nginx
nginx -t

# Перезапуск Nginx
systemctl restart nginx
```

### 10. Настройка файрвола (UFW)

```bash
# Разрешение HTTP и HTTPS
ufw allow 'Nginx Full'
ufw enable
```

### Дополнительные рекомендации

1. Безопасность:
   - Измените стандартные порты
   - Настройте SSL (Let's Encrypt)
   - Ограничьте права доступа

2. Мониторинг:
   - Настройте логирование
   - Используйте инструменты мониторинга

### Проверка работоспособности

```bash
# Просмотр логов Nginx
tail -f /var/log/nginx/error.log

# Просмотр логов Gunicorn
journalctl -u legal_assistant
```

### Возможные проблемы

- Проверьте права доступа к файлам
- Убедитесь, что все переменные корректны
- Проверьте логи при возникновении ошибок

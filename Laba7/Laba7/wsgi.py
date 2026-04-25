# Django WSGI конфигурация для развертывания проекта на production серверах
# WSGI (Web Server Gateway Interface) - интерфейс между веб-сервером и Django приложением

import os
from django.core.wsgi import get_wsgi_application

# Установка модуля параметров Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Laba7.settings')

# Получение WSGI приложения
application = get_wsgi_application()

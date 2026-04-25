"""WSGI-конфигурация проекта Laba8.

Используется при классическом запуске Django через WSGI-сервер.
"""

import os

from django.core.wsgi import get_wsgi_application


# Подключаем настройки проекта перед созданием WSGI-приложения.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "lab8site.settings")
application = get_wsgi_application()

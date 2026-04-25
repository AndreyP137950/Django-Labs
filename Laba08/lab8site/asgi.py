"""ASGI-конфигурация проекта Laba8.

Нужна для асинхронных серверов и совместимости Django с современными
веб-развертываниями.
"""

import os

from django.core.asgi import get_asgi_application


# Указываем настройки проекта до создания объекта ASGI-приложения.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "lab8site.settings")
application = get_asgi_application()

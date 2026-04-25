"""ASGI-конфигурация проекта.

Файл нужен для асинхронных серверов и современного развертывания Django.

Журнал изменений:
- DEV-AI01 | 2026-04-11 | Причина: унификация комментариев инфраструктурных модулей.
- Исходный фрагмент: отсутствовал формализованный блок об изменении.
"""

import os

from django.core.asgi import get_asgi_application


# Передаем Django имя файла настроек.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "lab6site.settings")


# Создаем ASGI-приложение.
application = get_asgi_application()

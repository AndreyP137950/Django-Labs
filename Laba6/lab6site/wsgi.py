"""WSGI-конфигурация проекта.

Этот модуль используется классическими веб-серверами для запуска Django.

Журнал изменений:
- DEV-AI01 | 2026-04-11 | Причина: унификация комментариев инфраструктурных модулей.
- Исходный фрагмент: отсутствовал формализованный блок об изменении.
"""

import os

from django.core.wsgi import get_wsgi_application


# Передаем Django имя файла настроек.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "lab6site.settings")


# Создаем WSGI-приложение.
application = get_wsgi_application()

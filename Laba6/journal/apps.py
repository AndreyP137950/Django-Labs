"""Описание приложения journal для Django.

Класс AppConfig нужен Django, чтобы зарегистрировать приложение в проекте.

Журнал изменений:
- DEV-AI01 | 2026-04-11 | Причина: унификация документирования модулей.
- Исходный фрагмент: не было блока истории изменений.
"""

from django.apps import AppConfig


class JournalConfig(AppConfig):
    """Конфигурация приложения Journal для автоподключения в Django."""

    # Внутреннее имя приложения.
    default_auto_field = "django.db.models.BigAutoField"
    # Человекочитаемое имя приложения.
    name = "journal"
    verbose_name = "Журнал заметок"

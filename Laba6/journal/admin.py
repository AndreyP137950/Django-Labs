"""Регистрация моделей в административной панели.

Через admin.py удобно проверять данные и управлять записями без отдельного UI.

Журнал изменений:
- DEV-AI01 | 2026-04-11 | Причина: дополнение служебных комментариев для ЛР6.
- Исходный фрагмент: не был указан формализованный блок об изменениях.
"""

from django.contrib import admin

from .models import JournalEntry


# Настраиваем вид списка записей в админ-панели.
@admin.register(JournalEntry)
class JournalEntryAdmin(admin.ModelAdmin):
    """Настройки отображения модели JournalEntry в Django Admin."""

    # Показываем ключевые поля в таблице.
    list_display = ("title", "priority", "created_at", "updated_at")
    # Добавляем быстрый поиск по заголовку и содержимому.
    search_fields = ("title", "content")
    # Позволяем фильтровать записи по приоритету и дате создания.
    list_filter = ("priority", "created_at")
    # Автоматически заполняем поле slug из заголовка.
    prepopulated_fields = {"slug": ("title",)}

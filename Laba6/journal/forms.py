"""Формы Django для приложения.

ModelForm позволяет связать HTML-форму с моделью без ручного описания всех полей.

Журнал изменений:
- DEV-AI01 | 2026-04-11 | Причина: усиление документирования формы для ЛР6.
- Исходный фрагмент: отсутствовал развернутый комментарий назначения класса формы.
"""

from django import forms

from .models import JournalEntry


# Форма для создания и редактирования записей журнала.
class JournalEntryForm(forms.ModelForm):
    """Форма ввода и редактирования данных JournalEntry.

    Форма используется двумя представлениями:
    - `EntryCreateView` для добавления новой записи.
    - `EntryUpdateView` для изменения существующей записи.
    """

    class Meta:
        # Указываем, с какой моделью связана форма.
        model = JournalEntry
        # Ограничиваем набор полей, чтобы форма была проще для лабораторной.
        fields = ["title", "slug", "content", "priority"]
        # Виджеты задают базовый HTML и минимальные стили для полей.
        widgets = {
            "title": forms.TextInput(attrs={"placeholder": "Краткий заголовок"}),
            "slug": forms.TextInput(attrs={"placeholder": "unikalnyy-identifikator"}),
            "content": forms.Textarea(attrs={"rows": 8, "placeholder": "Текст записи"}),
            "priority": forms.Select(),
        }
        # Подсказки помогают объяснить назначение каждого поля.
        help_texts = {
            "slug": "Используется в адресе страницы и должен быть уникальным.",
            "priority": "1 - высокий приоритет, 2 - обычный, 3 - низкий.",
        }

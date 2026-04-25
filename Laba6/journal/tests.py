"""Автоматические тесты для приложения.

Минимальный набор тестов нужен, чтобы проверить работу основных страниц и модели.

Журнал изменений:
- DEV-AI01 | 2026-04-11 | Причина: добавление расширенного документирования тестов.
- Исходный фрагмент: отсутствовали docstring-комментарии для класса и тестовых методов.
"""

from django.test import TestCase
from django.urls import reverse

from .models import JournalEntry


class JournalEntryTests(TestCase):
    """Набор проверок модели JournalEntry и маршрутов, связанных с ней."""

    # Проверяем, что объект модели создается и строковое представление работает.
    def test_model_str_and_url(self):
        """Проверяет строковое представление и формирование URL по slug."""

        entry = JournalEntry.objects.create(
            title="Тестовая запись",
            slug="testovaya-zapis",
            content="Проверка модели.",
            priority=1,
        )
        self.assertEqual(str(entry), "Тестовая запись")
        self.assertEqual(entry.get_absolute_url(), reverse("journal:entry_detail", kwargs={"slug": "testovaya-zapis"}))

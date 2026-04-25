"""Представления приложения.

Views принимают HTTP-запрос, подготавливают данные и возвращают HTML-ответ.

Журнал изменений:
- DEV-AI01 | 2026-04-11 | Причина: приведение комментариев к требованиям ЛР6.
- Исходный фрагмент: в методах отсутствовали развернутые docstring-описания
    входных параметров и результата.
"""

from django.contrib import messages
from django.db.models import Count
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from .forms import JournalEntryForm
from .models import JournalEntry


# Сводная страница приложения: список записей и краткая статистика.
class EntryListView(ListView):
    """Показывает главную страницу со списком записей и статистикой.

    Условия использования:
    - Метод доступен по URL главной страницы приложения.
    - В ответе формируется HTML на основе шаблона dashboard.
    """

    # Модель, которую будет отображать список.
    model = JournalEntry
    # Имя переменной в шаблоне.
    context_object_name = "entries"
    # Шаблон списка.
    template_name = "journal/dashboard.html"

    def get_context_data(self, **kwargs):
        """Дополняет контекст агрегированной статистикой.

        Аргументы:
            **kwargs: стандартные именованные параметры от базового класса.

        Возвращает:
            dict: контекст шаблона со списком записей и счетчиками.
        """

        # Получаем стандартный контекст от ListView.
        context = super().get_context_data(**kwargs)
        # Добавляем количество записей для информационного блока.
        context["entry_count"] = JournalEntry.objects.count()
        # Подсчитываем записи по приоритетам для демонстрации работы ORM.
        context["priority_stats"] = (
            JournalEntry.objects.values("priority").annotate(total=Count("id")).order_by("priority")
        )
        return context


# Страница с подробным просмотром одной записи.
class EntryDetailView(DetailView):
    """Отображает одну запись журнала по ее slug-идентификатору."""

    # Базовая модель для поиска объекта.
    model = JournalEntry
    # Используем slug вместо числового id в адресе.
    slug_field = "slug"
    slug_url_kwarg = "slug"
    # Шаблон подробной страницы.
    template_name = "journal/entry_detail.html"
    # Название переменной для шаблона.
    context_object_name = "entry"


# Создание новой записи через HTML-форму.
class EntryCreateView(CreateView):
    """Создает новую запись журнала через HTML-форму."""

    # Используем нашу форму, чтобы показать структуру данных.
    form_class = JournalEntryForm
    # Шаблон для страницы добавления.
    template_name = "journal/entry_form.html"

    def form_valid(self, form):
        """Сохраняет объект и добавляет сообщение об успешном создании.

        Аргументы:
            form (JournalEntryForm): валидная форма создания записи.

        Возвращает:
            HttpResponse: стандартный redirect-ответ CreateView.
        """

        # Сохраняем запись и показываем сообщение об успешном добавлении.
        response = super().form_valid(form)
        messages.success(self.request, "Запись успешно создана.")
        return response


# Редактирование существующей записи.
class EntryUpdateView(UpdateView):
    """Редактирует существующую запись журнала по slug."""

    # Используем ту же форму, что и при создании.
    form_class = JournalEntryForm
    # Шаблон для страницы редактирования.
    template_name = "journal/entry_form.html"
    # Ищем объект по slug.
    slug_field = "slug"
    slug_url_kwarg = "slug"

    def form_valid(self, form):
        """Сохраняет изменения и добавляет сообщение об обновлении.

        Аргументы:
            form (JournalEntryForm): валидная форма редактирования записи.

        Возвращает:
            HttpResponse: стандартный redirect-ответ UpdateView.
        """

        # После сохранения сообщаем пользователю о результатах.
        response = super().form_valid(form)
        messages.success(self.request, "Запись успешно обновлена.")
        return response


# Удаление записи с подтверждением.
class EntryDeleteView(DeleteView):
    """Удаляет запись журнала после подтверждения пользователя."""

    # Удаляем объект модели JournalEntry.
    model = JournalEntry
    # После удаления возвращаемся на главную страницу приложения.
    success_url = reverse_lazy("journal:dashboard")
    # Шаблон подтверждения удаления.
    template_name = "journal/entry_confirm_delete.html"
    # Поиск объекта выполняется по slug.
    slug_field = "slug"
    slug_url_kwarg = "slug"

    def delete(self, request, *args, **kwargs):
        """Удаляет выбранный объект и показывает уведомление.

        Аргументы:
            request (HttpRequest): текущий HTTP-запрос.
            *args: позиционные аргументы базового класса.
            **kwargs: именованные аргументы маршрута (включая slug).

        Возвращает:
            HttpResponse: redirect на страницу списка записей.
        """

        # Сохраняем ссылку на объект для сообщения после удаления.
        self.object = self.get_object()
        response = super().delete(request, *args, **kwargs)
        messages.success(request, f"Запись '{self.object.title}' удалена.")
        return response

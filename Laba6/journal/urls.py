"""Маршруты приложения journal.

Здесь URL-адреса связываются с конкретными классами представлений.

Журнал изменений:
- DEV-AI01 | 2026-04-11 | Причина: добавление служебного документирования в модуле URL.
- Исходный фрагмент: отсутствовал блок истории изменений.
"""

from django.urls import path

from .views import EntryCreateView, EntryDeleteView, EntryDetailView, EntryListView, EntryUpdateView


# Пространство имен помогает не путать маршруты разных приложений.
app_name = "journal"


# Таблица маршрутов приложения.
urlpatterns = [
    # Главная страница с обзором записей.
    path("", EntryListView.as_view(), name="dashboard"),
    # Страница подробного просмотра.
    path("entry/<slug:slug>/", EntryDetailView.as_view(), name="entry_detail"),
    # Форма создания записи.
    path("entry/add/", EntryCreateView.as_view(), name="entry_add"),
    # Форма редактирования записи.
    path("entry/<slug:slug>/edit/", EntryUpdateView.as_view(), name="entry_edit"),
    # Подтверждение удаления записи.
    path("entry/<slug:slug>/delete/", EntryDeleteView.as_view(), name="entry_delete"),
]

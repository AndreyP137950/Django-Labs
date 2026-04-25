"""
Главный URL конфиг для проекта case_designer
Маршрутизирует запросы на приложение designer
"""

from django.urls import path, include

urlpatterns = [
    # Все URL приложения designer подключаются в корень проекта.
    path('', include('designer.urls')),
]

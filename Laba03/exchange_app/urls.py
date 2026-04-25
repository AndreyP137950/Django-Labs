from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'), # Главная страница приложения
    path('api/source/save/', views.save_source_data, name='save_source_data'), # API для сохранения данных из Источника
    path('api/server/process/', views.process_server_data, name='process_server_data'), # API для обработки данных в Сервере
    path('api/visualizer/display/', views.display_in_excel, name='display_in_excel'), # API для отправки данных в Excel
]

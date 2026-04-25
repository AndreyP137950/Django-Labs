"""
URL маршруты приложения designer
"""

from django.urls import path
from . import views

app_name = 'designer'

urlpatterns = [
    # Главная страница конструктора
    path('', views.index, name='index'),
    
    # AJAX запросы
    path('api/calculate/', views.calculate, name='calculate'),
    path('api/generate-vba/', views.generate_vba, name='generate_vba'),
    path('api/download-vba/', views.download_vba, name='download_vba'),
    path('api/save-chain/', views.save_chain, name='save_chain'),
]

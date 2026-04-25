# Маршруты URL приложения assets
# Связывает URLs с соответствующими представлениями (views)

from django.urls import path
from . import views

# Маршруты приложения
urlpatterns = [
    # Главная страница
    path('', views.index, name='index'),
    
    # ==================== МАРШРУТЫ ПОДРАЗДЕЛЕНИЙ ====================
    
    # Список подразделений
    path('departments/', views.DepartmentListView.as_view(), name='department_list'),
    
    # Создание нового подразделения
    path('departments/create/', views.DepartmentCreateView.as_view(), name='department_create'),
    
    # Детали подразделения
    path('departments/<int:pk>/', views.DepartmentDetailView.as_view(), name='department_detail'),
    
    # Редактирование подразделения
    path('departments/<int:pk>/edit/', views.DepartmentUpdateView.as_view(), name='department_update'),
    
    # Удаление подразделения
    path('departments/<int:pk>/delete/', views.DepartmentDeleteView.as_view(), name='department_delete'),
    
    # ==================== МАРШРУТЫ ОСНОВНЫХ СРЕДСТВ ====================
    
    # Список основных средств
    path('assets/', views.FixedAssetListView.as_view(), name='fixedasset_list'),
    
    # Создание нового основного средства
    path('assets/create/', views.FixedAssetCreateView.as_view(), name='fixedasset_create'),
    
    # Детали основного средства
    path('assets/<int:pk>/', views.FixedAssetDetailView.as_view(), name='fixedasset_detail'),
    
    # Редактирование основного средства
    path('assets/<int:pk>/edit/', views.FixedAssetUpdateView.as_view(), name='fixedasset_update'),
    
    # Удаление основного средства
    path('assets/<int:pk>/delete/', views.FixedAssetDeleteView.as_view(), name='fixedasset_delete'),
    
    # AJAX маршрут для переназначения кода внутреннего учета
    path('assets/<int:pk>/assign-code/', views.assign_internal_code, name='assign_internal_code'),
]

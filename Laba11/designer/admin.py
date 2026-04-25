"""
Администрирование приложения designer
Здесь регистрируются модели для управления через Django admin

Администратор может быть создан командой:
python manage.py createsuperuser
"""

from django.contrib import admin
from .models import FunctionChain

@admin.register(FunctionChain)
class FunctionChainAdmin(admin.ModelAdmin):
    """
    Администраторский интерфейс для модели FunctionChain
    Позволяет просматривать и редактировать сохраненные цепочки функций
    """
    
    # Поля для отображения в списке
    list_display = ('id', 'function_f1', 'function_f2', 'function_f3', 'created_at', 'description')
    
    # Фильтры для быстрого поиска
    list_filter = ('function_f1', 'function_f2', 'function_f3', 'created_at')
    
    # Поля для поиска
    search_fields = ('description',)
    
    # Только чтение для времени создания
    readonly_fields = ('created_at',)
    
    # Организация полей в форме
    fieldsets = (
        ('Конфигурация функций', {
            'fields': ('function_f1', 'function_f2', 'function_f3')
        }),
        ('Информация', {
            'fields': ('created_at', 'description')
        }),
    )
    
    def __str__(self):
        return f"Цепочка #{self.id}"

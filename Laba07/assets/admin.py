# Администрирование приложения assets
# Конфигурирует отображение моделей в админ-панели Django

from django.contrib import admin
from .models import Department, FixedAsset

# Регистрация модели "Подразделение" в админ-панели
@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    """Администрирование подразделений"""
    
    # Какие поля выводить в списке подразделений
    list_display = ('code', 'name', 'created_at')
    
    # Поля, по которым можно осуществлять поиск
    search_fields = ('code', 'name')
    
    # Поля, по которым можно фильтровать
    list_filter = ('created_at',)
    
    # Порядок полей при редактировании
    fieldsets = (
        ('Основная информация', {
            'fields': ('code', 'name', 'description')
        }),
    )
    
    # Только для чтения - нельзя менять значения
    readonly_fields = ('created_at',)


# Регистрация модели "Основное средство" в админ-панели
@admin.register(FixedAsset)
class FixedAssetAdmin(admin.ModelAdmin):
    """Администрирование основных средств"""
    
    # Какие поля выводить в списке
    list_display = (
        'internal_code', 
        'name', 
        'department', 
        'cost', 
        'depreciation_percent',
        'purchase_date'
    )
    
    # Поля для поиска
    search_fields = ('name', 'internal_code', 'department__name')
    
    # Фильтрация по полям
    list_filter = ('department', 'purchase_date', 'created_at')
    
    # Группировка полей при редактировании
    fieldsets = (
        ('Основная информация', {
            'fields': ('name', 'description', 'department')
        }),
        ('Финансовая информация', {
            'fields': ('cost', 'depreciation_percent', 'purchase_date')
        }),
        ('Код внутреннего учета', {
            'fields': ('internal_code', 'sequence_number'),
            'description': 'Код генерируется автоматически при создании'
        }),
        ('Служебная информация', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)  # Скрытый по умолчанию раздел
        }),
    )
    
    # Поля только для чтения
    readonly_fields = ('internal_code', 'sequence_number', 'created_at', 'updated_at')
    
    def save_model(self, request, obj, form, change):
        """Сохранение модели при редактировании через админ-панель"""
        # Если это новый объект и internal_code еще не установлен
        if not obj.internal_code:
            obj.generate_internal_code()
        super().save_model(request, obj, form, change)

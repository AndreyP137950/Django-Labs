# Представления (Views) приложения assets
# Обрабатывают HTTP запросы и возвращают ответы (HTML страницы)

from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Q, Max
from .models import Department, FixedAsset
from .forms import DepartmentForm, FixedAssetForm


# ==================== ПРЕДСТАВЛЕНИЯ ДЛЯ ГЛАВНОЙ СТРАНИЦЫ ====================

def index(request):
    """
    Главная страница приложения
    Выводит статистику по основным средствам и подразделениям
    """
    
    # Получаем статистику
    context = {
        # Общее количество основных средств
        'total_assets': FixedAsset.objects.count(),
        # Общее количество подразделений
        'total_departments': Department.objects.count(),
        # Общая стоимость всех ОС
        'total_cost': sum(asset.cost for asset in FixedAsset.objects.all()),
        # Последние добавленные ОС (для информационной ленты)
        'recent_assets': FixedAsset.objects.all().order_by('-created_at')[:5],
    }
    
    return render(request, 'assets/index.html', context)


# ==================== ПРЕДСТАВЛЕНИЯ ДЛЯ ПОДРАЗДЕЛЕНИЙ ====================

class DepartmentListView(ListView):
    """
    Список всех подразделений организации
    Выводит таблицу со всеми подразделениями и кнопками действий
    """
    
    # Используемая модель
    model = Department
    # Имя переменной контекста в шаблоне
    context_object_name = 'departments'
    # Имя шаблона для отображения
    template_name = 'assets/department_list.html'
    # Количество объектов на странице (для пагинации)
    paginate_by = 20


class DepartmentDetailView(DetailView):
    """
    Детальная страница подразделения
    Выводит информацию о подразделении и список его ОС
    """
    
    model = Department
    context_object_name = 'department'
    template_name = 'assets/department_detail.html'
    
    def get_context_data(self, **kwargs):
        """Добавляем дополнительные данные в контекст"""
        context = super().get_context_data(**kwargs)
        # Получаем все ОС текущего подразделения
        context['assets'] = self.object.assets.all()
        # Количество ОС в подразделении
        context['assets_count'] = self.object.assets.count()
        # Общая стоимость ОС в подразделении
        context['assets_total_cost'] = sum(asset.cost for asset in self.object.assets.all())
        return context


class DepartmentCreateView(CreateView):
    """
    Создание нового подразделения
    Форма с полями: код, наименование, описание
    """
    
    model = Department
    form_class = DepartmentForm
    template_name = 'assets/department_form.html'
    success_url = reverse_lazy('department_list')
    
    def form_valid(self, form):
        """После успешного заполнения формы"""
        # Преобразуем код в верхний регистр
        form.instance.code = form.instance.code.upper()
        # Сохраняем форму и выводим сообщение об успехе
        response = super().form_valid(form)
        messages.success(self.request, f'Подразделение "{self.object.name}" успешно создано')
        return response


class DepartmentUpdateView(UpdateView):
    """
    Редактирование подразделения
    Форма для изменения параметров подразделения
    """
    
    model = Department
    form_class = DepartmentForm
    template_name = 'assets/department_form.html'
    success_url = reverse_lazy('department_list')
    
    def form_valid(self, form):
        """После успешного редактирования"""
        form.instance.code = form.instance.code.upper()
        response = super().form_valid(form)
        messages.success(self.request, f'Подразделение "{self.object.name}" успешно обновлено')
        return response


class DepartmentDeleteView(DeleteView):
    """
    Удаление подразделения
    При удалении подразделения удаляются и все его ОС
    """
    
    model = Department
    template_name = 'assets/department_confirm_delete.html'
    success_url = reverse_lazy('department_list')
    
    def delete(self, request, *args, **kwargs):
        """При удалении показываем сообщение"""
        self.object = self.get_object()
        messages.success(request, f'Подразделение "{self.object.name}" и все его ОС удалены')
        return super().delete(request, *args, **kwargs)


# ==================== ПРЕДСТАВЛЕНИЯ ДЛЯ ОСНОВНЫХ СРЕДСТВ ====================

class FixedAssetListView(ListView):
    """
    Список всех основных средств
    Выводит таблицу со всеми ОС и их внутренними кодами
    """
    
    model = FixedAsset
    context_object_name = 'assets'
    template_name = 'assets/fixedasset_list.html'
    paginate_by = 20
    
    def get_queryset(self):
        """Получение списка оС может быть отфильтровано"""
        queryset = FixedAsset.objects.select_related('department')
        
        # Поиск по названию или коду
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) | 
                Q(internal_code__icontains=search)
            )
        
        # Фильтрация по подразделению
        department = self.request.GET.get('department')
        if department:
            queryset = queryset.filter(department__id=department)
        
        return queryset.order_by('-created_at')
    
    def get_context_data(self, **kwargs):
        """Добавляем список подразделений для фильтра"""
        context = super().get_context_data(**kwargs)
        context['departments'] = Department.objects.all()
        context['search'] = self.request.GET.get('search', '')
        return context


class FixedAssetDetailView(DetailView):
    """
    Детальная страница основного средства
    Выводит всю информацию об ОС
    """
    
    model = FixedAsset
    context_object_name = 'asset'
    template_name = 'assets/fixedasset_detail.html'


class FixedAssetCreateView(CreateView):
    """
    Создание нового основного средства
    Форма с автоматическим заполнением кода внутреннего учета
    """
    
    model = FixedAsset
    form_class = FixedAssetForm
    template_name = 'assets/fixedasset_form.html'
    success_url = reverse_lazy('fixedasset_list')
    
    def form_valid(self, form):
        """После успешного заполнения формы"""
        # Если нажата кнопка "Назначить внутренний код"
        # или это просто создание нового ОС
        if self.request.POST.get('assign_code') == 'true' or not form.instance.internal_code:
            # Генерируем внутренний код автоматически
            form.instance.generate_internal_code()
        
        response = super().form_valid(form)
        messages.success(
            self.request, 
            f'Основное средство "{self.object.name}" создано с кодом {self.object.internal_code}'
        )
        return response


class FixedAssetUpdateView(UpdateView):
    """
    Редактирование основного средства
    Форма для изменения параметров ОС
    """
    
    model = FixedAsset
    form_class = FixedAssetForm
    template_name = 'assets/fixedasset_form.html'
    success_url = reverse_lazy('fixedasset_list')
    
    def form_valid(self, form):
        """После успешного редактирования"""
        # Если нажата кнопка переназначения кода
        if self.request.POST.get('assign_code') == 'true':
            # Зануляем старый код и генерируем новый
            form.instance.internal_code = ''
            form.instance.generate_internal_code()
        
        response = super().form_valid(form)
        messages.success(self.request, 'Основное средство успешно обновлено')
        return response


class FixedAssetDeleteView(DeleteView):
    """
    Удаление основного средства
    При удалении освобождается слот порядковый номер
    """
    
    model = FixedAsset
    template_name = 'assets/fixedasset_confirm_delete.html'
    success_url = reverse_lazy('fixedasset_list')
    
    def delete(self, request, *args, **kwargs):
        """При удалении показываем сообщение"""
        self.object = self.get_object()
        messages.success(request, f'Основное средство "{self.object.name}" удалено')
        return super().delete(request, *args, **kwargs)


# ==================== ФУНКЦИЯ ДЛЯ AJAX ЗАПРОСА ====================

def assign_internal_code(request, pk):
    """
    AJAX функция для переназначения кода внутреннего учета
    Переполучает максимальный номер и генерирует новый код
    
    Args:
        request: HTTP запрос
        pk: ID основного средства
    
    Returns:
        JSON с новым кодом или ошибкой
    """
    
    try:
        # Получаем ОС по ID
        asset = FixedAsset.objects.get(pk=pk)
        
        # Генерируем новый код
        old_code = asset.internal_code
        asset.generate_internal_code()
        asset.save()
        
        # Возвращаем результат в JSON формате
        return JsonResponse({
            'success': True,
            'old_code': old_code,
            'new_code': asset.internal_code,
            'message': f'Код переназначен: {old_code} → {asset.internal_code}'
        })
    
    except FixedAsset.DoesNotExist:
        return JsonResponse({
            'success': False,
            'error': 'Основное средство не найдено'
        }, status=404)
    
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)

"""
Представления (views) для приложения Case системы

Описание:
- index: Основная страница конструктора
- calculate: Вычисление результата цепочки функций
- generate_vba: Генерирование VBA кода
- save_chain: Сохранение цепочки функций
"""

import json
from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_http_methods
from .models import FunctionChain, FUNCTION_TYPES

def index(request):
    """
    Главная страница Case системы - конструктор функций
    Позволяет визуально выбирать функции и конфигурировать цепочку
    """
    # Получаем последнюю созданную цепочку или создаем новую.
    try:
        chain = FunctionChain.objects.latest('created_at')
    except FunctionChain.DoesNotExist:
        chain = FunctionChain.objects.create()
    
    context = {
        'chain': chain,
        'function_types': FUNCTION_TYPES,
        'functions_display': chain.get_functions_display(),
    }
    
    return render(request, 'designer/index.html', context)

@require_http_methods(["POST"])
def calculate(request):
    """
    AJAX запрос для вычисления результата цепочки функций
    
    POST параметры:
        x_value (float): Входное значение x
        f1 (str): Функция F1
        f2 (str): Функция F2
        f3 (str): Функция F3
    
    Возвращает:
        JSON с результатом вычисления и описанием шагов
    """
    try:
        # Читаем параметры из POST-запроса и подготавливаем вычисление.
        x_value = float(request.POST.get('x_value', 0))
        f1 = request.POST.get('f1', 'sqrt')
        f2 = request.POST.get('f2', 'reciprocal')
        f3 = request.POST.get('f3', 'exp')
        
        # Создаем временную цепочку для вычисления.
        chain = FunctionChain(
            function_f1=f1,
            function_f2=f2,
            function_f3=f3
        )
        
        # Вычисляем результат.
        result = chain.calculate(x_value)
        
        return JsonResponse({
            'success': True,
            'result': result['result'],
            'error': result['error'],
            'steps': result['steps'],
        })
    
    except ValueError:
        return JsonResponse({
            'success': False,
            'error': 'Ошибка: введите корректное числовое значение'
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': f'Ошибка сервера: {str(e)}'
        })

@require_http_methods(["POST"])
def generate_vba(request):
    """
    AJAX запрос для генерирования VBA кода
    
    POST параметры:
        f1 (str): Функция F1
        f2 (str): Функция F2
        f3 (str): Функция F3
    
    Возвращает:
        JSON с VBA кодом
    """
    try:
        # Читаем параметры функций из запроса.
        f1 = request.POST.get('f1', 'sqrt')
        f2 = request.POST.get('f2', 'reciprocal')
        f3 = request.POST.get('f3', 'exp')
        
        # Создаем цепочку для генерации VBA.
        chain = FunctionChain(
            function_f1=f1,
            function_f2=f2,
            function_f3=f3
        )
        
        # Генерируем VBA код.
        vba_code = chain.generate_vba_code()
        
        return JsonResponse({
            'success': True,
            'vba_code': vba_code,
        })
    
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': f'Ошибка генерирования кода: {str(e)}'
        })

@require_http_methods(["POST"])
def download_vba(request):
    """
    Загрузить VBA код как файл .bas для импорта в Excel
    
    POST параметры:
        f1 (str): Функция F1
        f2 (str): Функция F2
        f3 (str): Функция F3
    
    Возвращает:
        VBA файл для скачивания
    """
    try:
        # Читаем параметры функций и описание.
        f1 = request.POST.get('f1', 'sqrt')
        f2 = request.POST.get('f2', 'reciprocal')
        f3 = request.POST.get('f3', 'exp')
        
        # Создаем цепочку
        chain = FunctionChain(
            function_f1=f1,
            function_f2=f2,
            function_f3=f3
        )
        
        # Генерируем VBA код
        vba_code = chain.generate_vba_code()
        
        # Возвращаем как скачиваемый файл
        response = HttpResponse(vba_code, content_type='text/plain')
        response['Content-Disposition'] = 'attachment; filename="case_functions.bas"'
        
        return response
    
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': f'Ошибка: {str(e)}'
        })

@require_http_methods(["POST"])
def save_chain(request):
    """
    Сохранить конфигурацию цепочки функций в базу данных
    
    POST параметры:
        f1 (str): Функция F1
        f2 (str): Функция F2
        f3 (str): Функция F3
        description (str): Описание (опционально)
    
    Возвращает:
        JSON с ID сохраненной цепочки
    """
    try:
        # Получаем параметры
        f1 = request.POST.get('f1', 'sqrt')
        f2 = request.POST.get('f2', 'reciprocal')
        f3 = request.POST.get('f3', 'exp')
        description = request.POST.get('description', '')
        
        # Создаем и сохраняем цепочку
        chain = FunctionChain.objects.create(
            function_f1=f1,
            function_f2=f2,
            function_f3=f3,
            description=description
        )
        
        return JsonResponse({
            'success': True,
            'chain_id': chain.id,
            'message': 'Цепочка успешно сохранена'
        })
    
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': f'Ошибка сохранения: {str(e)}'
        })

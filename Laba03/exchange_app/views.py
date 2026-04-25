import json
import os
from collections import defaultdict
from django.shortcuts import render
from django.http import JsonResponse
from django.conf import settings

# Определяем путь к файлу обмена данных
EXCHANGE_FILE_PATH = os.path.join(settings.BASE_DIR, 'export_data.json')

def index(request):
    """
    Главная страница, на которой отображаются три блока:
    1. Источник (генерация и выгрузка)
    2. Сервер (прием и обработка)
    3. Визуализатор (отправка в Excel)
    """
    return render(request, 'exchange_app/index.html')

def save_source_data(request):
    """
    Представление для сохранения данных из Источника.
    Получает JSON структуру и данные, сохраняет их во внешний файл export_data.json.
    """
    if request.method == 'POST':
        try:
            body = json.loads(request.body)
            # Структура данных (описывает поля: какие передавать, типы данных и т.д.)
            structure = body.get('structure', [])
            # Сами данные
            data = body.get('data', [])
            
            # Сохраняем в файл по формату JSON
            export_content = {
                'structure': structure,
                'data': data
            }
            
            with open(EXCHANGE_FILE_PATH, 'w', encoding='utf-8') as f:
                json.dump(export_content, f, ensure_ascii=False, indent=4)
                
            return JsonResponse({'status': 'success', 'message': 'Данные успешно сохранены во внешний файл.'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    return JsonResponse({'status': 'error', 'message': 'Только POST запросы'}, status=405)

def process_server_data(request):
    """
    Представление Сервера. 
    Читает файл export_data.json, выполняет обработку (усреднение курса на дату).
    """
    if request.method == 'GET':
        if not os.path.exists(EXCHANGE_FILE_PATH):
            return JsonResponse({'status': 'error', 'message': 'Файл данных не найден. Сначала выгрузите данные из Источника.'}, status=404)
            
        try:
            with open(EXCHANGE_FILE_PATH, 'r', encoding='utf-8') as f:
                content = json.load(f)
                
            structure = content.get('structure', [])
            data = content.get('data', [])
            
            # Определяем какие поля нужно передавать
            fields_to_transmit = {field['code']: field for field in structure if field.get('transmit')}
            
            if 'date' not in fields_to_transmit or 'rate' not in fields_to_transmit:
                return JsonResponse({
                    'status': 'error', 
                    'message': 'В структуре отсутствуют обязательные поля (date, rate) или для них не установлен признак передачи.'
                }, status=400)

            # Выполняем обработку: усреднение значения курса на каждую дату
            # Исходные данные: Дата, Курс, Биржа, и т.д.
            date_rates = defaultdict(list)
            
            for row in data:
                date_val = row.get('date')
                try:
                    rate_val = float(row.get('rate', 0))
                except ValueError:
                    continue # Пропускаем если курс не число
                
                if date_val:
                    date_rates[date_val].append(rate_val)
                    
            # Усредняем и форматируем дату (ДД.ММ.ГГГГ)
            from datetime import datetime
            processed_data = []
            for d, rates in date_rates.items():
                avg_rate = sum(rates) / len(rates)
                
                try:
                    dt = datetime.strptime(d, '%d.%m.%Y')
                    """
                    try:
                        # ДД.ММ.ГГГГ
                        dt = datetime.strptime(d, '%d.%m.%Y')
                    except ValueError:
                        # Старый формат (если остались старые данные): ГГГГ-ММ-ДД
                        dt = datetime.strptime(d, '%Y-%m-%d')
                        """
                    formatted_date = dt.strftime('%d.%m.%Y')
                    # Формат YYYY-MM-DD оставляем для правильной сортировки строк
                    sort_date = dt.strftime('%Y-%m-%d')
                except Exception:
                    formatted_date = d
                    sort_date = d

                processed_data.append({
                    'original_date': sort_date,  # Сохраняем ISO 8601 для правильной сортировки хронологии
                    'date': formatted_date,
                    'avg_rate': round(avg_rate, 4)
                })
                
            # Сортируем по хронологии для красивого отображения графика
            processed_data.sort(key=lambda x: x['original_date'])
            
            return JsonResponse({'status': 'success', 'processed_data': processed_data})
            
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    return JsonResponse({'status': 'error', 'message': 'Только GET запросы'}, status=405)

def display_in_excel(request):
    """
    Представление для визуализатора.
    Получает обработанные данные, связывается с Excel через win32com и рисует график.
    """
    if request.method == 'POST':
        try:
            body = json.loads(request.body)
            processed_data = body.get('processed_data', [])
            
            if not processed_data:
                return JsonResponse({'status': 'error', 'message': 'Нет данных для визуализации'}, status=400)

            # Подключаем OLE API (win32com)
            import pywin32_system32 # Инициализация пути (иногда требуется)
            import pythoncom
            import win32com.client
            
            # Инициализация COM-библиотек для текущего потока (Django обрабатывает запросы в разных потоках)
            pythoncom.CoInitialize()
            
            # Создаем объект Excel
            excel = win32com.client.Dispatch('Excel.Application')
            
            # Создаем новую книгу
            workbook = excel.Workbooks.Add()
            sheet = workbook.Worksheets(1)
            
            # Заполняем заголовки
            sheet.Cells(1, 1).Value = "Дата"
            sheet.Cells(1, 2).Value = "Средний курс"
            
            # Заполняем данные
            row_idx = 2
            for row in processed_data:
                sheet.Cells(row_idx, 1).Value = row['date']
                sheet.Cells(row_idx, 2).Value = row['avg_rate']
                row_idx += 1
                
            # Форматируем границы
            used_range = sheet.Range(f"A1:B{row_idx-1}")
            used_range.Columns.AutoFit()
            
            # Рисуем диаграмму по заполненным данным
            chart = excel.Charts.Add()
            # Тип графика - линия с маркерами (xlLineMarkers = 65)
            chart.ChartType = 65 
            chart.SetSourceData(Source=used_range)
            # Название диаграммы
            chart.HasTitle = True
            chart.ChartTitle.Text = "Динамика усредненного курса доллара по биржам"
            
            # Делаем Excel видимым пользователю
            excel.Visible = True
            
            return JsonResponse({'status': 'success', 'message': 'Excel успешно запущен, данные визуализированы.'})
        except Exception as e:
            import traceback
            error_details = traceback.format_exc()
            return JsonResponse({'status': 'error', 'message': f'Ошибка при работе с Excel: {str(e)}', 'details': error_details}, status=500)
    return JsonResponse({'status': 'error', 'message': 'Только POST запросы'}, status=405)

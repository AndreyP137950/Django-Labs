"""
Модели для Case системы проектирования математических функций

Описание:
- FunctionChain: Цепочка функций y = F1(F2(F3(x)))
- FunctionType: Тип функции (sqrt, reciprocal, exp)
"""

import json
import math
from django.db import models

# Доступные функции в системе.
FUNCTION_TYPES = [
    ('sqrt', 'Корень квадратный (sqrt)'),
    ('reciprocal', 'Обратная функция (1/x)'),
    ('exp', 'Экспоненциальная функция (e^x)'),
]

class FunctionChain(models.Model):
    """
    Модель для хранения цепочки функций
    Структура: y = F1(F2(F3(x)))
    """
    # Выбор функций для трех этапов вычисления.
    function_f1 = models.CharField(
        max_length=20,
        choices=FUNCTION_TYPES,
        default='sqrt',
        verbose_name='Функция F1 (вторая внешняя функция)'
    )
    
    function_f2 = models.CharField(
        max_length=20,
        choices=FUNCTION_TYPES,
        default='reciprocal',
        verbose_name='Функция F2 (средняя функция)'
    )
    
    function_f3 = models.CharField(
        max_length=20,
        choices=FUNCTION_TYPES,
        default='exp',
        verbose_name='Функция F3 (внутренняя функция)'
    )
    
    # Дата создания цепочки.
    created_at = models.DateTimeField(auto_now_add=True)
    
    # Описание (заметки пользователя).
    description = models.TextField(blank=True, null=True)
    
    class Meta:
        verbose_name = 'Цепочка функций'
        verbose_name_plural = 'Цепочки функций'
    
    def __str__(self):
        return f"F1({self.function_f1}) -> F2({self.function_f2}) -> F3({self.function_f3})"
    
    def get_functions_display(self):
        """Возвращает словарь названий функций для отображения"""
        return {
            'F1': dict(FUNCTION_TYPES)[self.function_f1],
            'F2': dict(FUNCTION_TYPES)[self.function_f2],
            'F3': dict(FUNCTION_TYPES)[self.function_f3],
        }
    
    @staticmethod
    def apply_function(func_name, value):
        """
        Применяет функцию к значению
        
        Аргументы:
            func_name (str): Название функции ('sqrt', 'reciprocal', 'exp')
            value (float): Входное значение
        
        Возвращает:
            tuple: (результат, ошибка) где результат = None если есть ошибка
        """
        try:
            if func_name == 'sqrt':
                # Корень квадратный: область определения x >= 0
                if value < 0:
                    return None, "Ошибка: Аргумент корня не может быть отрицательным"
                return math.sqrt(value), None
            
            elif func_name == 'reciprocal':
                # Обратная функция 1/x: область определения x != 0
                if value == 0:
                    return None, "Ошибка: Деление на ноль не допускается"
                return 1 / value, None
            
            elif func_name == 'exp':
                # Экспоненциальная функция e^x: область определения все реальные числа
                return math.exp(value), None
            
            else:
                return None, f"Неизвестная функция: {func_name}"
        
        except Exception as e:
            return None, f"Ошибка вычисления: {str(e)}"
    
    def calculate(self, x_value):
        """
        Вычисляет результат цепочки функций y = F1(F2(F3(x)))
        
        Аргументы:
            x_value (float): Входное значение x
        
        Возвращает:
            dict: {'result': значение или None, 'error': сообщение об ошибке или None, 
                   'steps': [шаги вычисления]}
        """
        steps = []
        
        # Шаг 1: Применяем F3(x)
        result, error = self.apply_function(self.function_f3, x_value)
        if error:
            return {
                'result': None,
                'error': f"F3({x_value}): {error}",
                'steps': steps
            }
        steps.append(f"F3({x_value}) = {result}")
        
        # Шаг 2: Применяем F2(результат F3)
        result, error = self.apply_function(self.function_f2, result)
        if error:
            return {
                'result': None,
                'error': f"F2(...): {error}",
                'steps': steps
            }
        steps.append(f"F2(...) = {result}")
        
        # Шаг 3: Применяем F1(результат F2)
        result, error = self.apply_function(self.function_f1, result)
        if error:
            return {
                'result': None,
                'error': f"F1(...): {error}",
                'steps': steps
            }
        steps.append(f"F1(...) = {result}")
        
        return {
            'result': result,
            'error': None,
            'steps': steps
        }
    
    def generate_vba_code(self):
        """
        Генерирует VBA программный код для реализации цепочки функций в Excel
        
        Возвращает:
            str: VBA код
        """
        vba_code = '''' ========================================
' Автоматически сгенерированный код
' CASE система проектирования программ
' Лабораторная работа №11
' ========================================

    Option Explicit

Function sqrt_func(x As Double) As Double
    ' Функция корня квадратного
    ' Область определения: x >= 0
    If x < 0 Then
        MsgBox "Ошибка: аргумент корня не может быть отрицательным", vbCritical
        sqrt_func = 0
        Exit Function
    End If
    sqrt_func = Sqr(x)
End Function

Function reciprocal_func(x As Double) As Double
    ' Функция обратная 1/x
    ' Область определения: x <> 0
    If x = 0 Then
        MsgBox "Ошибка: деление на ноль не допускается", vbCritical
        reciprocal_func = 0
        Exit Function
    End If
    reciprocal_func = 1 / x
End Function

Function exp_func(x As Double) As Double
    ' Экспоненциальная функция e^x
    ' Область определения: все реальные числа
    exp_func = Exp(x)
End Function

Function CalculateChain(x As Double) As Double
    ' Главная функция для вычисления цепочки: y = F1(F2(F3(x)))
    ' Аргумент: x - входное значение
    ' Возвращает: результат y
    
    Dim step1 As Double, step2 As Double, step3 As Double
    
    ' Шаг 1: Вычислим F3(x)
    step1 = ''' + self._get_function_call(self.function_f3, 'x') + '''
    
    ' Шаг 2: Вычислим F2(F3(x))
    step2 = ''' + self._get_function_call(self.function_f2, 'step1') + '''
    
    ' Шаг 3: Вычислим F1(F2(F3(x)))
    step3 = ''' + self._get_function_call(self.function_f1, 'step2') + '''
    
    ' Результат
    CalculateChain = step3
End Function

Sub TestCalculate()
    ' Подпрограмма для тестирования
    ' Введите значение x в ячейку A1, результат появится в A2
    
    Dim x As Double
    Dim result As Double
    
    x = Range("A1").Value
    result = CalculateChain(x)
    
    Range("A2").Value = result
    MsgBox "Результат: " & result, vbInformation
End Sub

Sub Graph()
    ' Подпрограмма для построения графика по рассчитанным значениям

    Dim ws As Worksheet
    Dim chartObj As ChartObject
    Dim xMin As Double
    Dim xMax As Double
    Dim stepSize As Double
    Dim answer As Variant
    Dim x As Double
    Dim rowIndex As Long
    Dim lastRow As Long

    answer = Application.InputBox("Введите xMin:", "Построение графика", Type:=1)
    If VarType(answer) = vbBoolean And answer = False Then Exit Sub
    xMin = CDbl(answer)

    answer = Application.InputBox("Введите xMax:", "Построение графика", Type:=1)
    If VarType(answer) = vbBoolean And answer = False Then Exit Sub
    xMax = CDbl(answer)

    answer = Application.InputBox("Введите шаг:", "Построение графика", Type:=1)
    If VarType(answer) = vbBoolean And answer = False Then Exit Sub
    stepSize = CDbl(answer)

    If stepSize <= 0 Then
        MsgBox "Ошибка: шаг должен быть больше 0", vbCritical
        Exit Sub
    End If

    If xMax < xMin Then
        MsgBox "Ошибка: xMax должен быть больше или равен xMin", vbCritical
        Exit Sub
    End If

    Set ws = ActiveSheet
    ws.Range("A:B").ClearContents
    ws.Cells(1, 1).Value = "x"
    ws.Cells(1, 2).Value = "y"

    rowIndex = 2
    For x = xMin To xMax Step stepSize
        ws.Cells(rowIndex, 1).Value = x
        ws.Cells(rowIndex, 2).Value = CalculateChain(x)
        rowIndex = rowIndex + 1
    Next x

    lastRow = rowIndex - 1
    If lastRow < 2 Then
        MsgBox "Ошибка: недостаточно точек для построения графика", vbCritical
        Exit Sub
    End If

    If ws.ChartObjects.Count > 0 Then
        ws.ChartObjects(1).Delete
    End If

    Set chartObj = ws.ChartObjects.Add(Left:=300, Top:=10, Width:=500, Height:=300)
    With chartObj.Chart
        .ChartType = xlXYScatterLines
        .HasTitle = True
        .ChartTitle.Text = "y = F1(F2(F3(x)))"
        .SeriesCollection.NewSeries
        .SeriesCollection(1).Name = "y"
        .SeriesCollection(1).XValues = ws.Range(ws.Cells(2, 1), ws.Cells(lastRow, 1))
        .SeriesCollection(1).Values = ws.Range(ws.Cells(2, 2), ws.Cells(lastRow, 2))
        .Axes(xlCategory).HasTitle = True
        .Axes(xlCategory).AxisTitle.Text = "x"
        .Axes(xlValue).HasTitle = True
        .Axes(xlValue).AxisTitle.Text = "y"
    End With
End Sub
'''
        
        return vba_code
    
    def _get_function_call(self, func_name, arg):
        """
        Возвращает строку вызова функции в VBA
        
        Аргументы:
            func_name (str): Название функции
            arg (str): Аргумент функции
        
        Возвращает:
            str: Строка VBA кода для вызова функции
        """
        if func_name == 'sqrt':
            return f'sqrt_func({arg})'
        elif func_name == 'reciprocal':
            return f'reciprocal_func({arg})'
        elif func_name == 'exp':
            return f'exp_func({arg})'
        else:
            return f'{arg}'

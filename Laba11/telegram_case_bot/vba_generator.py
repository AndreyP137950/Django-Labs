"""Генератор VBA-кода для выбранной цепочки функций."""

from __future__ import annotations


def _vba_call(func_name: str, arg: str) -> str:
    """Возвращает вызов VBA-функции по имени математической функции."""
    if func_name == "sqrt":
        return f"sqrt_func({arg})"
    if func_name == "reciprocal":
        return f"reciprocal_func({arg})"
    if func_name == "exp":
        return f"exp_func({arg})"
    return arg


def generate_vba_code(f1: str, f2: str, f3: str) -> str:
    """Формирует готовый VBA-код, который можно вставить в модуль Excel."""
    # Выстраиваем цепочку вызовов в порядке F3 -> F2 -> F1.
    step1 = _vba_call(f3, "x")
    step2 = _vba_call(f2, "step1")
    step3 = _vba_call(f1, "step2")

    return f"""' ========================================
' Автоматически сгенерированный код
' Лабораторная работа №11
' Выражение: y = F1(F2(F3(x)))
' ========================================

Option Explicit

Function sqrt_func(x As Double) As Double
    If x < 0 Then
        MsgBox "Ошибка: аргумент для sqrt(x) должен быть >= 0", vbCritical
        sqrt_func = 0
        Exit Function
    End If
    sqrt_func = Sqr(x)
End Function

Function reciprocal_func(x As Double) As Double
    If x = 0 Then
        MsgBox "Ошибка: деление на ноль", vbCritical
        reciprocal_func = 0
        Exit Function
    End If
    reciprocal_func = 1 / x
End Function

Function exp_func(x As Double) As Double
    exp_func = Exp(x)
End Function

Function CalculateChain(x As Double) As Double
    Dim step1 As Double, step2 As Double, step3 As Double

    step1 = {step1}
    step2 = {step2}
    step3 = {step3}

    CalculateChain = step3
End Function

Sub TestCalculate()
    Dim x As Double
    Dim result As Double

    x = Range("A1").Value
    result = CalculateChain(x)

    Range("A2").Value = result
    MsgBox "Результат: " & result, vbInformation
End Sub

Sub Graph()
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
"""

"""Математическая логика для CASE-бота.

Задача: вычислять выражение y = F1(F2(F3(x)))
где каждая функция выбирается из набора: sqrt, reciprocal, exp.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Callable


FUNCTIONS = ("sqrt", "reciprocal", "exp")


@dataclass
class CalcResult:
    """Результат вычисления цепочки функций."""

    value: float | None
    error: str | None
    steps: list[str]


def _apply(func_name: str, x: float) -> tuple[float | None, str | None]:
    """Применяет одну функцию к значению и валидирует область определения."""
    if func_name == "sqrt":
        if x < 0:
            return None, "Аргумент для sqrt(x) должен быть >= 0."
        return math.sqrt(x), None

    if func_name == "reciprocal":
        if x == 0:
            return None, "Для 1/x аргумент не может быть равен 0."
        return 1 / x, None

    if func_name == "exp":
        return math.exp(x), None

    return None, f"Неизвестная функция: {func_name}"


def calculate_chain(f1: str, f2: str, f3: str, x: float) -> CalcResult:
    """Вычисляет y = F1(F2(F3(x))) с пошаговым журналом."""
    steps: list[str] = []

    r1, e1 = _apply(f3, x)
    if e1 is not None:
        return CalcResult(value=None, error=f"Ошибка на этапе F3: {e1}", steps=steps)
    steps.append(f"F3({x}) = {r1}")

    r2, e2 = _apply(f2, r1)
    if e2 is not None:
        return CalcResult(value=None, error=f"Ошибка на этапе F2: {e2}", steps=steps)
    steps.append(f"F2({r1}) = {r2}")

    r3, e3 = _apply(f1, r2)
    if e3 is not None:
        return CalcResult(value=None, error=f"Ошибка на этапе F1: {e3}", steps=steps)
    steps.append(f"F1({r2}) = {r3}")

    return CalcResult(value=r3, error=None, steps=steps)


def human_formula(f1: str, f2: str, f3: str) -> str:
    """Возвращает человекочитаемую формулу текущей конфигурации."""
    return f"y = {f1}({f2}({f3}(x)))"

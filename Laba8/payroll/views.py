"""Представления приложения payroll.

Здесь находится главная страница, список начислений в виде печатной формы,
а также CRUD-страницы для удобного заполнения учебных данных.
"""

from decimal import Decimal, InvalidOperation

from django.contrib import messages
from django.db.models import Sum
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, TemplateView, UpdateView

from .forms import SalaryAccrualForm
from .models import SalaryAccrual


# Значения по умолчанию для цветовой логики отчета.
DEFAULT_LOWER_LIMIT = Decimal("30000")
DEFAULT_UPPER_LIMIT = Decimal("60000")
DEFAULT_DIVISOR = 5


def _parse_decimal(value: str | None, default: Decimal) -> Decimal:
    """Безопасно превращает строку из GET-параметра в Decimal."""
    if value in (None, ""):
        return default
    try:
        return Decimal(value)
    except (InvalidOperation, TypeError):
        return default


def _parse_int(value: str | None, default: int) -> int:
    """Безопасно превращает строку из GET-параметра в int."""
    if value in (None, ""):
        return default
    try:
        parsed = int(value)
    except (TypeError, ValueError):
        return default
    return parsed if parsed > 0 else default


def _build_row(accrual: SalaryAccrual, position: int, lower_limit: Decimal, upper_limit: Decimal, divisor: int) -> dict:
    """Создает данные строки отчета с классами для подсветки."""
    amount = accrual.amount

    if amount > upper_limit:
        amount_state = "high"
        amount_label = "Выше верхнего порога"
    elif amount < lower_limit:
        amount_state = "low"
        amount_label = "Ниже нижнего порога"
    else:
        amount_state = "middle"
        amount_label = "Между порогами"

    # Кратность показываем отдельным индикатором, чтобы визуально не смешивать
    # две разные проверки: по сумме и по делению на число.
    if divisor and amount % Decimal(divisor) == 0:
        divisibility_state = "multiple"
        divisibility_label = f"Кратно {divisor}"
    else:
        divisibility_state = "not-multiple"
        divisibility_label = f"Не кратно {divisor}"

    return {
        "position": position,
        "accrual": accrual,
        "amount_state": amount_state,
        "amount_label": amount_label,
        "divisibility_state": divisibility_state,
        "divisibility_label": divisibility_label,
    }


class HomeView(TemplateView):
    """Главная страница лабораторной работы."""

    template_name = "payroll/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        accruals = SalaryAccrual.objects.all()
        context["accrual_count"] = accruals.count()
        context["total_amount"] = accruals.aggregate(total=Sum("amount"))["total"] or Decimal("0")
        context["recent_accruals"] = accruals.order_by("-id")[:5]
        return context


class SalaryAccrualListView(ListView):
    """Печатная форма отчета по всем сотрудникам."""

    model = SalaryAccrual
    template_name = "payroll/report.html"
    context_object_name = "accruals"

    def get_queryset(self):
        return SalaryAccrual.objects.all().order_by("id")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        lower_limit = _parse_decimal(self.request.GET.get("lower"), DEFAULT_LOWER_LIMIT)
        upper_limit = _parse_decimal(self.request.GET.get("upper"), DEFAULT_UPPER_LIMIT)
        divisor = _parse_int(self.request.GET.get("divisor"), DEFAULT_DIVISOR)

        accrual_rows = [
            _build_row(accrual, position, lower_limit, upper_limit, divisor)
            for position, accrual in enumerate(self.object_list, start=1)
        ]

        context.update(
            {
                "accrual_rows": accrual_rows,
                "lower_limit": lower_limit,
                "upper_limit": upper_limit,
                "divisor": divisor,
                "total_amount": sum((row["accrual"].amount for row in accrual_rows), Decimal("0")),
                "page_title": "Отчет по всем сотрудникам",
            }
        )
        return context


class SalaryAccrualPrintView(SalaryAccrualListView):
    """Печатная версия отчета без лишней навигации."""

    template_name = "payroll/report_print.html"


class SalaryAccrualDetailView(DetailView):
    """Детальная страница одной записи начисления."""

    model = SalaryAccrual
    template_name = "payroll/accrual_detail.html"
    context_object_name = "accrual"


class SalaryAccrualCreateView(CreateView):
    """Создание новой записи начисления."""

    model = SalaryAccrual
    form_class = SalaryAccrualForm
    template_name = "payroll/accrual_form.html"

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, f'Начисление для сотрудника "{self.object.employee}" сохранено.')
        return response


class SalaryAccrualUpdateView(UpdateView):
    """Редактирование существующей записи начисления."""

    model = SalaryAccrual
    form_class = SalaryAccrualForm
    template_name = "payroll/accrual_form.html"

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, f'Начисление для сотрудника "{self.object.employee}" обновлено.')
        return response


class SalaryAccrualDeleteView(DeleteView):
    """Удаление записи начисления."""

    model = SalaryAccrual
    template_name = "payroll/accrual_confirm_delete.html"
    success_url = reverse_lazy("payroll:report")

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        messages.success(request, f'Начисление для сотрудника "{self.object.employee}" удалено.')
        return super().delete(request, *args, **kwargs)

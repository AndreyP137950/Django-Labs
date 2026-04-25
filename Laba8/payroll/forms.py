"""Формы приложения payroll.

Форма используется для ручного добавления и редактирования начислений
через веб-интерфейс и Django admin.
"""

from django import forms

from .models import SalaryAccrual


class SalaryAccrualForm(forms.ModelForm):
    """Форма для одной записи начисления зарплаты."""

    class Meta:
        # Используем только поля, которые вводятся пользователем в веб-форме.
        model = SalaryAccrual
        fields = ["employee", "amount", "comment"]
        widgets = {
            "employee": forms.TextInput(attrs={"class": "form-input", "placeholder": "Фамилия и имя сотрудника"}),
            "amount": forms.NumberInput(attrs={"class": "form-input", "step": "0.01", "min": "0"}),
            "comment": forms.TextInput(attrs={"class": "form-input", "placeholder": "Необязательно"}),
        }
        help_texts = {
            "employee": "Введите имя сотрудника так, как оно должно печататься в отчете.",
            "amount": "Число с двумя знаками после запятой.",
            "comment": "Краткая пометка для удобства учета.",
        }

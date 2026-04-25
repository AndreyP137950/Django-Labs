"""Модели предметной области для лабораторной работы №8.

В этой работе справочник из 1С заменен на таблицу Django с начислениями
зарплаты сотрудникам, чтобы реализовать печатную форму в веб-приложении.
"""

from django.core.validators import MinValueValidator
from django.db import models
from django.urls import reverse


class SalaryAccrual(models.Model):
    """Запись начисления зарплаты одному сотруднику."""

    # Имя сотрудника, по которому строится отчет.
    employee = models.CharField("Сотрудник", max_length=120)
    # Сумма начисления в денежном выражении.
    amount = models.DecimalField(
        "Начислено",
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(0)],
    )
    # Дата создания записи начисления.
    accrual_date = models.DateField("Дата начисления", auto_now_add=True)
    # Необязательная заметка для внутреннего учета.
    comment = models.CharField("Комментарий", max_length=255, blank=True)

    class Meta:
        verbose_name = "Начисление зарплаты"
        verbose_name_plural = "Начисления зарплаты"
        ordering = ["employee", "id"]

    def __str__(self) -> str:
        return f"{self.employee}: {self.amount}"

    def get_absolute_url(self):
        """Нужен для перехода на детальную страницу после сохранения."""
        return reverse("payroll:accrual_detail", kwargs={"pk": self.pk})

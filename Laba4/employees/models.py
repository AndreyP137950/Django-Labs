from django.db import models
from django.urls import reverse

class Employee(models.Model):
    last_name = models.CharField(max_length=100, verbose_name="Фамилия")
    first_name = models.CharField(max_length=100, verbose_name="Имя")
    patronymic = models.CharField(max_length=100, blank=True, verbose_name="Отчество")
    position = models.CharField(max_length=150, verbose_name="Должность")
    address = models.CharField(max_length=255, verbose_name="Адрес")
    personal_phone = models.CharField(max_length=20, verbose_name="Личный телефон")
    work_phone = models.CharField(max_length=20, blank=True, verbose_name="Рабочий телефон")

    class Meta:
        verbose_name = "Сотрудник"
        verbose_name_plural = "Сотрудники"
        ordering = ['last_name', 'first_name'] # Сортировка по умолчанию по фамилии и имени
        # Определяем кастомные права доступа, чтобы их можно было назначать группам
        permissions = [
            # Права создаются автоматически (add_employee, change_employee, delete_employee, view_employee),
            # Но можно добавить свои, если нужно
        ]

    def __str__(self):
        # Строковое представление объекта для админки и других выводов
        return f"{self.last_name} {self.first_name} {self.patronymic}".strip()

    def get_absolute_url(self):
        # Метод для получения URL конкретного сотрудника (обычно нужен, но у нас пока простой список)
        return reverse('employee_list')

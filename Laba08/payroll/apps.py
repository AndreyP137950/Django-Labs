from django.apps import AppConfig


class PayrollConfig(AppConfig):
    """Конфигурация приложения для учета начислений."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "payroll"
    verbose_name = "Начисление зарплаты"

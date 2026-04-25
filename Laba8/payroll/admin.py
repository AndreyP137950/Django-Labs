"""Настройки админ-панели для модели начислений."""

from django.contrib import admin

from .models import SalaryAccrual


@admin.register(SalaryAccrual)
class SalaryAccrualAdmin(admin.ModelAdmin):
    """Удобный список записей для редактирования через Django Admin."""

    list_display = ("employee", "amount", "accrual_date", "comment")
    search_fields = ("employee", "comment")
    list_filter = ("accrual_date",)
    ordering = ("employee",)
    readonly_fields = ("accrual_date",)
    fieldsets = (
        (None, {"fields": ("employee", "amount")} ),
        ("Дополнительно", {"fields": ("comment", "accrual_date")} ),
    )

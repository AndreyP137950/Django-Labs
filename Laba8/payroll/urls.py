"""URL-маршруты приложения payroll."""

from django.urls import path

from .views import (
    HomeView,
    SalaryAccrualCreateView,
    SalaryAccrualDetailView,
    SalaryAccrualDeleteView,
    SalaryAccrualListView,
    SalaryAccrualPrintView,
    SalaryAccrualUpdateView,
)

app_name = "payroll"

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("report/", SalaryAccrualListView.as_view(), name="report"),
    path("report/print/", SalaryAccrualPrintView.as_view(), name="report_print"),
    path("accrual/add/", SalaryAccrualCreateView.as_view(), name="accrual_add"),
    path("accrual/<int:pk>/", SalaryAccrualDetailView.as_view(), name="accrual_detail"),
    path("accrual/<int:pk>/edit/", SalaryAccrualUpdateView.as_view(), name="accrual_edit"),
    path("accrual/<int:pk>/delete/", SalaryAccrualDeleteView.as_view(), name="accrual_delete"),
]

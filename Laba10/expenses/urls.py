from django.urls import path

from .views import expense_report_view

app_name = 'expenses'

urlpatterns = [
    path('', expense_report_view, name='report'),
]

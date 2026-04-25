"""Корневой URL-конфиг проекта Laba8."""

from django.contrib import admin
from django.urls import include, path


urlpatterns = [
    # Административная панель Django.
    path("admin/", admin.site.urls),
    # Корневой маршрут ведет в приложение payroll.
    path("", include("payroll.urls")),
]

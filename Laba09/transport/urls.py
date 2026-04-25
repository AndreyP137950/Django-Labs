from django.urls import path

from .views import (
    TripSheetCreateView,
    cars_list,
    charts_view,
    driver_cars_api,
    drivers_list,
    home,
    trip_sheets_list,
)

app_name = 'transport'

urlpatterns = [
    path('', home, name='home'),
    path('drivers/', drivers_list, name='drivers_list'),
    path('cars/', cars_list, name='cars_list'),
    path('trip-sheets/', trip_sheets_list, name='trip_sheets_list'),
    path('trip-sheets/new/', TripSheetCreateView.as_view(), name='trip_sheet_create'),
    path('charts/', charts_view, name='charts'),
    path('api/drivers/<int:driver_id>/cars/', driver_cars_api, name='driver_cars_api'),
]

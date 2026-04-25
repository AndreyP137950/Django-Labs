from django.contrib import admin

from .models import Car, Driver, Employee, TripSheet


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
	list_display = ('full_name',)
	search_fields = ('full_name',)


@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
	list_display = ('brand', 'plate_number', 'production_year', 'fuel_rate_per_km')
	search_fields = ('brand', 'plate_number')


@admin.register(Driver)
class DriverAdmin(admin.ModelAdmin):
	list_display = ('employee',)
	filter_horizontal = ('cars',)
	search_fields = ('employee__full_name',)


@admin.register(TripSheet)
class TripSheetAdmin(admin.ModelAdmin):
	list_display = (
		'driver',
		'car',
		'departure_time',
		'arrival_time',
		'mileage',
		'fuel_consumption',
	)
	list_filter = ('car', 'driver', 'departure_time')
	search_fields = ('driver__employee__full_name', 'car__brand', 'car__plate_number')

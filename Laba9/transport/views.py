from decimal import Decimal

from django.db.models import Avg, Sum
from django.db.models.functions import Coalesce
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.views.generic import CreateView

from .forms import TripSheetForm
from .models import Car, Driver, TripSheet


def home(request):
	# Сводные показатели по системе учета.
	summary = {
		'drivers_count': Driver.objects.count(),
		'cars_count': Car.objects.count(),
		'trip_count': TripSheet.objects.count(),
		'total_mileage': TripSheet.objects.aggregate(total=Coalesce(Sum('mileage'), Decimal('0.0')))['total'],
		'total_fuel': TripSheet.objects.aggregate(total=Coalesce(Sum('fuel_consumption'), Decimal('0.000')))['total'],
	}
	return render(request, 'transport/home.html', {'summary': summary})


def drivers_list(request):
	drivers = Driver.objects.select_related('employee').annotate(
		total_mileage=Coalesce(Sum('trip_sheets__mileage'), Decimal('0.0'))
	)
	return render(request, 'transport/drivers_list.html', {'drivers': drivers})


def cars_list(request):
	cars = Car.objects.annotate(
		total_fuel=Coalesce(Sum('trip_sheets__fuel_consumption'), Decimal('0.000'))
	)
	return render(request, 'transport/cars_list.html', {'cars': cars})


def trip_sheets_list(request):
	trip_sheets = TripSheet.objects.select_related('driver__employee', 'car')
	return render(request, 'transport/trip_sheets_list.html', {'trip_sheets': trip_sheets})


class TripSheetCreateView(CreateView):
	model = TripSheet
	form_class = TripSheetForm
	template_name = 'transport/trip_sheet_form.html'
	success_url = '/trip-sheets/'


def driver_cars_api(request, driver_id):
	# API для динамического обновления списка машин на форме путевого листа.
	driver = get_object_or_404(Driver, pk=driver_id)
	cars_data = [{'id': car.id, 'title': str(car)} for car in driver.cars.all()]
	return JsonResponse({'cars': cars_data})


def charts_view(request):
	# Данные для диаграммы пробегов по водителям.
	drivers = Driver.objects.select_related('employee').annotate(
		total_mileage=Coalesce(Sum('trip_sheets__mileage'), Decimal('0.0'))
	)
	driver_labels = [item.employee.full_name for item in drivers]
	driver_values = [float(item.total_mileage) for item in drivers]
	avg_driver_mileage = float(
		Driver.objects.annotate(total=Coalesce(Sum('trip_sheets__mileage'), Decimal('0.0'))).aggregate(
			avg=Coalesce(Avg('total'), Decimal('0.0'))
		)['avg']
	)

	# Данные для диаграммы расхода топлива по автомобилям.
	cars = Car.objects.annotate(total_fuel=Coalesce(Sum('trip_sheets__fuel_consumption'), Decimal('0.000')))
	car_labels = [str(item) for item in cars]
	car_values = [float(item.total_fuel) for item in cars]
	avg_car_fuel = float(
		Car.objects.annotate(total=Coalesce(Sum('trip_sheets__fuel_consumption'), Decimal('0.000'))).aggregate(
			avg=Coalesce(Avg('total'), Decimal('0.0'))
		)['avg']
	)

	context = {
		'driver_labels': driver_labels,
		'driver_values': driver_values,
		'avg_driver_mileage': avg_driver_mileage,
		'car_labels': car_labels,
		'car_values': car_values,
		'avg_car_fuel': avg_car_fuel,
	}
	return render(request, 'transport/charts.html', context)

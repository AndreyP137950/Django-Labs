from datetime import timedelta
from decimal import Decimal

from django.core.exceptions import ValidationError
from django.test import TestCase
from django.utils import timezone

from .models import Car, Driver, Employee, TripSheet


class TripSheetModelTests(TestCase):
	# Проверяем ключевую логику: расчет пробега и расхода топлива.
	def test_trip_sheet_calculates_mileage_and_fuel(self):
		employee = Employee.objects.create(full_name='Тестовый Сотрудник')
		driver = Driver.objects.create(employee=employee)
		car = Car.objects.create(
			brand='TestCar',
			plate_number='Т001ТТ77',
			production_year=2020,
			fuel_rate_per_km=Decimal('0.100'),
		)
		driver.cars.add(car)

		start = timezone.now()
		sheet = TripSheet.objects.create(
			driver=driver,
			car=car,
			departure_time=start,
			arrival_time=start + timedelta(hours=1),
			start_km=Decimal('100.0'),
			end_km=Decimal('160.0'),
		)

		self.assertEqual(sheet.mileage, Decimal('60.0'))
		self.assertEqual(sheet.fuel_consumption, Decimal('6.000'))

	# Проверяем запрет на сохранение документа для незакрепленного автомобиля.
	def test_trip_sheet_validates_driver_car_pair(self):
		employee = Employee.objects.create(full_name='Другой Сотрудник')
		driver = Driver.objects.create(employee=employee)
		car = Car.objects.create(
			brand='OtherCar',
			plate_number='Т002ТТ77',
			production_year=2022,
			fuel_rate_per_km=Decimal('0.095'),
		)

		start = timezone.now()
		sheet = TripSheet(
			driver=driver,
			car=car,
			departure_time=start,
			arrival_time=start + timedelta(hours=1),
			start_km=Decimal('10.0'),
			end_km=Decimal('20.0'),
		)

		with self.assertRaises(ValidationError):
			sheet.full_clean()

# Create your tests here.

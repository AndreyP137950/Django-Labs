from decimal import Decimal

from django.core.exceptions import ValidationError
from django.db import models


class Employee(models.Model):
	# Справочник сотрудников используется как основа для водителей.
	# Храним сотрудника отдельно, чтобы его можно было использовать в разных справочниках.
	full_name = models.CharField(max_length=150, unique=True, verbose_name='Сотрудник')

	class Meta:
		verbose_name = 'Сотрудник'
		verbose_name_plural = 'Сотрудники'
		ordering = ['full_name']

	def __str__(self):
		return self.full_name


class Car(models.Model):
	# Автомобили привязываются к водителям и участвуют в путевых листах.
	brand = models.CharField(max_length=120, verbose_name='Марка автомобиля')
	plate_number = models.CharField(max_length=20, unique=True, verbose_name='Гос. номер')
	production_year = models.PositiveIntegerField(verbose_name='Год выпуска')
	fuel_rate_per_km = models.DecimalField(
		max_digits=6,
		decimal_places=3,
		verbose_name='Норма расхода (л/км)',
	)

	class Meta:
		verbose_name = 'Автомобиль'
		verbose_name_plural = 'Автомобили'
		ordering = ['brand', 'plate_number']

	def __str__(self):
		return f'{self.brand} ({self.plate_number})'


class Driver(models.Model):
	# Водитель связан с сотрудником один к одному и хранит доступные автомобили.
	employee = models.OneToOneField(
		Employee,
		on_delete=models.CASCADE,
		related_name='driver_profile',
		verbose_name='Сотрудник',
	)
	cars = models.ManyToManyField(Car, related_name='drivers', verbose_name='Автомобили')

	class Meta:
		verbose_name = 'Водитель'
		verbose_name_plural = 'Водители'
		ordering = ['employee__full_name']

	def __str__(self):
		return self.employee.full_name


class TripSheet(models.Model):
	# Путевой лист хранит выезд, заезд, пробег и расход топлива.
	driver = models.ForeignKey(
		Driver,
		on_delete=models.PROTECT,
		related_name='trip_sheets',
		verbose_name='Водитель',
	)
	car = models.ForeignKey(
		Car,
		on_delete=models.PROTECT,
		related_name='trip_sheets',
		verbose_name='Автомобиль',
	)
	departure_time = models.DateTimeField(verbose_name='Время выезда')
	arrival_time = models.DateTimeField(verbose_name='Время заезда')
	start_km = models.DecimalField(max_digits=10, decimal_places=1, verbose_name='Начальный километраж')
	end_km = models.DecimalField(max_digits=10, decimal_places=1, verbose_name='Конечный километраж')
	mileage = models.DecimalField(
		max_digits=10,
		decimal_places=1,
		editable=False,
		default=Decimal('0.0'),
		verbose_name='Пробег',
	)
	fuel_consumption = models.DecimalField(
		max_digits=10,
		decimal_places=3,
		editable=False,
		default=Decimal('0.000'),
		verbose_name='Расход топлива',
	)
	created_at = models.DateTimeField(auto_now_add=True)

	class Meta:
		verbose_name = 'Путевой лист'
		verbose_name_plural = 'Путевые листы'
		ordering = ['-departure_time', '-created_at']

	def __str__(self):
		return f'Путевой лист: {self.driver} - {self.car}'

	def clean(self):
		# Проверка корректности связи водитель-автомобиль и временных интервалов.
		if self.arrival_time <= self.departure_time:
			raise ValidationError('Время заезда должно быть позже времени выезда.')

		if self.end_km < self.start_km:
			raise ValidationError('Конечный километраж не может быть меньше начального.')

		if self.driver_id and self.car_id and not self.driver.cars.filter(pk=self.car_id).exists():
			raise ValidationError('Выбранный автомобиль не закреплен за этим водителем.')

	def save(self, *args, **kwargs):
		# Вычисляемые поля пересчитываются при каждом сохранении документа.
		self.full_clean()
		self.mileage = self.end_km - self.start_km
		self.fuel_consumption = self.mileage * self.car.fuel_rate_per_km
		super().save(*args, **kwargs)

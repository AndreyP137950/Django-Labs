from datetime import timedelta
from decimal import Decimal

from django.core.management.base import BaseCommand
from django.utils import timezone

from transport.models import Car, Driver, Employee, TripSheet


class Command(BaseCommand):
    help = 'Заполняет БД демонстрационными данными под требования варианта 1.'

    def handle(self, *args, **options):
        # Очищаем документы, чтобы пересоздать набор данных в предсказуемом виде.
        TripSheet.objects.all().delete()
        Driver.objects.all().delete()
        Employee.objects.all().delete()
        Car.objects.all().delete()

        # Сотрудники и водители.
        emp_ivanov = Employee.objects.create(full_name='Иванов Иван Иванович')
        emp_petrov = Employee.objects.create(full_name='Петров Петр Петрович')
        emp_sidorov = Employee.objects.create(full_name='Сидоров Сидор Сидорович')

        driver_ivanov = Driver.objects.create(employee=emp_ivanov)
        driver_petrov = Driver.objects.create(employee=emp_petrov)
        driver_sidorov = Driver.objects.create(employee=emp_sidorov)

        # Автомобили справочника.
        car_a = Car.objects.create(
            brand='ГАЗель Next',
            plate_number='А111АА77',
            production_year=2020,
            fuel_rate_per_km=Decimal('0.120'),
        )
        car_b = Car.objects.create(
            brand='Ford Transit',
            plate_number='В222ВВ77',
            production_year=2021,
            fuel_rate_per_km=Decimal('0.105'),
        )
        car_c = Car.objects.create(
            brand='Lada Largus',
            plate_number='С333СС77',
            production_year=2019,
            fuel_rate_per_km=Decimal('0.090'),
        )

        # Связи водитель-автомобиль по условиям задания.
        # Один автомобиль (car_a) закреплен за двумя водителями.
        # Один водитель (driver_ivanov) закреплен за двумя автомобилями.
        driver_ivanov.cars.set([car_a, car_b])
        driver_petrov.cars.set([car_a])
        driver_sidorov.cars.set([car_c])

        base_time = timezone.now() - timedelta(days=1)

        # Пробег Иванова делаем самым большим.
        TripSheet.objects.create(
            driver=driver_ivanov,
            car=car_a,
            departure_time=base_time,
            arrival_time=base_time + timedelta(hours=3),
            start_km=Decimal('12500.0'),
            end_km=Decimal('12620.0'),
        )
        TripSheet.objects.create(
            driver=driver_ivanov,
            car=car_b,
            departure_time=base_time + timedelta(hours=5),
            arrival_time=base_time + timedelta(hours=8),
            start_km=Decimal('8450.0'),
            end_km=Decimal('8540.0'),
        )
        TripSheet.objects.create(
            driver=driver_petrov,
            car=car_a,
            departure_time=base_time + timedelta(hours=2),
            arrival_time=base_time + timedelta(hours=4),
            start_km=Decimal('12620.0'),
            end_km=Decimal('12670.0'),
        )
        TripSheet.objects.create(
            driver=driver_sidorov,
            car=car_c,
            departure_time=base_time + timedelta(hours=1),
            arrival_time=base_time + timedelta(hours=2, minutes=30),
            start_km=Decimal('19000.0'),
            end_km=Decimal('19035.0'),
        )

        self.stdout.write(self.style.SUCCESS('Демонстрационные данные успешно созданы.'))

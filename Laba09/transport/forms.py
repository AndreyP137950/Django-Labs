from django import forms

from .models import Car, Driver, TripSheet


class TripSheetForm(forms.ModelForm):
    # Используем HTML5 datetime-local, чтобы ввод времени был удобным.
    departure_time = forms.DateTimeField(
        label='Время выезда',
        input_formats=['%Y-%m-%dT%H:%M'],
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}),
    )
    arrival_time = forms.DateTimeField(
        label='Время заезда',
        input_formats=['%Y-%m-%dT%H:%M'],
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}),
    )

    class Meta:
        model = TripSheet
        fields = ['driver', 'car', 'departure_time', 'arrival_time', 'start_km', 'end_km']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Список водителей показываем с загруженными сотрудниками.
        self.fields['driver'].queryset = Driver.objects.select_related('employee')
        # Машины подставляем только после выбора водителя.
        self.fields['car'].queryset = Car.objects.none()

        # Серверная фильтрация списка автомобилей по выбранному водителю.
        driver_id = self.data.get('driver') or self.initial.get('driver')
        if driver_id:
            try:
                driver = Driver.objects.get(pk=driver_id)
                self.fields['car'].queryset = driver.cars.all()
            except (Driver.DoesNotExist, ValueError, TypeError):
                self.fields['car'].queryset = Car.objects.none()
        elif self.instance.pk:
            self.fields['car'].queryset = self.instance.driver.cars.all()

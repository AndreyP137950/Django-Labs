# Формы Django приложения assets
# Используются для отображения и обработки HTML форм при редактировании/создании ОС

from django import forms
from django.core.exceptions import ValidationError

from .models import Department, FixedAsset

# Форма для создания и редактирования подразделения.
class DepartmentForm(forms.ModelForm):
    """Форма для создания/редактирования подразделения"""
    
    class Meta:
        model = Department
        # Какие поля выводить в форме
        fields = ['code', 'name', 'description']
        
        # Кастомизация виджетов (элементов HTML формы)
        widgets = {
            'code': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Например: ОФ, ЦЕХ1, ОТД2',
                'maxlength': '10'
            }),
            'name': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Наименование подразделения'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-textarea',
                'placeholder': 'Описание подразделения',
                'rows': 4
            }),
        }
    
    def clean_code(self):
        """Валидация кода подразделения"""
        code = self.cleaned_data.get('code')
        # Преобразуем в верхний регистр для стандартизации
        if code:
            code = code.upper()
        return code


# Форма для создания и редактирования основного средства.
class FixedAssetForm(forms.ModelForm):
    """
    Форма для создания/редактирования основного средства
    
    Содержит поле для кнопки "Назначить внутренний код"
    """
    
    # Дополнительное поле для кнопки (не сохраняется в БД)
    assign_code_button = forms.BooleanField(
        required=False,
        label='Назначить внутренний код',
        widget=forms.CheckboxInput(attrs={
            'class': 'button-checkbox',
            'style': 'display:none;'  # Скрываем чекбокс, так как используем кнопку
        })
    )
    
    class Meta:
        model = FixedAsset
        # Какие поля выводить в форме
        exclude = ['internal_code', 'sequence_number']
        
        # Кастомизация виджетов (элементов HTML формы)
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Наименование основного средства',
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-textarea',
                'placeholder': 'Описание',
                'rows': 3
            }),
            'department': forms.Select(attrs={
                'class': 'form-select',
            }),
            'purchase_date': forms.DateInput(attrs={
                'class': 'form-input',
                'type': 'date',
            }),
            'cost': forms.NumberInput(attrs={
                'class': 'form-input',
                'placeholder': 'Стоимость в рублях',
                'step': '0.01',
                'min': '0'
            }),
            'depreciation_percent': forms.NumberInput(attrs={
                'class': 'form-input',
                'placeholder': 'Процент износа (0-100%)',
                'min': '0',
                'max': '100'
            }),
        }
    
    def clean_cost(self):
        """Валидация стоимости"""
        cost = self.cleaned_data.get('cost')
        if cost and cost <= 0:
            raise ValidationError('Стоимость должна быть больше 0')
        return cost
    
    def clean_depreciation_percent(self):
        """Валидация процента износа"""
        depreciation = self.cleaned_data.get('depreciation_percent')
        if depreciation is not None:
            if not (0 <= depreciation <= 100):
                raise ValidationError('Процент износа должен быть от 0 до 100%')
        return depreciation
    
    def clean(self):
        """Общая валидация формы"""
        cleaned_data = super().clean()
        purchase_date = cleaned_data.get('purchase_date')
        
        # Проверяем, что дата покупки не в будущем
        from datetime import date
        if purchase_date and purchase_date > date.today():
            raise ValidationError('Дата покупки не может быть в будущем')
        
        return cleaned_data

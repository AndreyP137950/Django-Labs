from django import forms
from .models import Employee

class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['last_name', 'first_name', 'patronymic', 'position', 'address', 'personal_phone', 'work_phone']
        
        # Виджеты позволяют добавить CSS-классы для красивого отображения формы
        widgets = {
            'last_name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Иванов'}),
            'first_name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Иван'}),
            'patronymic': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Иванович'}),
            'position': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Должность'}),
            'address': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Адрес'}),
            'personal_phone': forms.TextInput(attrs={'class': 'form-input', 'placeholder': '+7 (XXX) XXX-XX-XX'}),
            'work_phone': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Внутренний номер'}),
        }

from django import forms


class ExpenseReportForm(forms.Form):
    # Период отчета: начало интервала (включительно).
    start_date = forms.DateField(
        label='Дата начала',
        widget=forms.DateInput(attrs={'type': 'date'}),
    )
    # Период отчета: конец интервала (включительно).
    end_date = forms.DateField(
        label='Дата окончания',
        widget=forms.DateInput(attrs={'type': 'date'}),
    )

    def clean(self):
        cleaned_data = super().clean()
        # Проверяем, что пользователь не перепутал начало и конец периода.
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')

        # Базовая проверка корректности интервала дат.
        if start_date and end_date and start_date > end_date:
            raise forms.ValidationError('Дата начала не может быть позже даты окончания.')

        return cleaned_data

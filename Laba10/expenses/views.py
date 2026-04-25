from decimal import Decimal

from django.db.models import Sum
from django.shortcuts import render
from django.utils import timezone

from .forms import ExpenseReportForm
from .models import Expense


def expense_report_view(request):
	# По умолчанию показываем текущий месяц, чтобы отчет открывался с полезными данными.
	today = timezone.localdate()
	initial_data = {
		'start_date': today.replace(day=1),
		'end_date': today,
	}

	form = ExpenseReportForm(request.GET or None, initial=initial_data)
	report_rows = []
	total_amount = Decimal('0.00')

	if form.is_valid():
		start_date = form.cleaned_data['start_date']
		end_date = form.cleaned_data['end_date']

		# Группируем записи по статье издержек и считаем сумму по каждой статье за период.
		queryset = (
			Expense.objects.filter(expense_date__range=(start_date, end_date))
			.values('category__name')
			.annotate(total=Sum('amount'))
			.order_by('category__name')
		)

		report_rows = list(queryset)
		total_amount = sum((row['total'] for row in report_rows), Decimal('0.00'))

	context = {
		'form': form,
		'report_rows': report_rows,
		'total_amount': total_amount,
	}
	return render(request, 'expenses/report.html', context)

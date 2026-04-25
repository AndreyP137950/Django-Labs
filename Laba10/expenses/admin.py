from django.contrib import admin

from .models import Expense, ExpenseCategory


@admin.register(ExpenseCategory)
class ExpenseCategoryAdmin(admin.ModelAdmin):
	# Быстрый поиск и сортировка по справочнику статей.
	list_display = ('name',)
	search_fields = ('name',)


@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
	# Табличное отображение операций издержек для ручного заполнения.
	list_display = ('expense_date', 'category', 'amount', 'note')
	list_filter = ('category', 'expense_date')
	search_fields = ('category__name', 'note')

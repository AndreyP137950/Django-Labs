from django.db import models


class ExpenseCategory(models.Model):
	# Справочник категорий нужен для группировки отчета.
	name = models.CharField(max_length=120, unique=True, verbose_name='Статья издержек')

	class Meta:
		verbose_name = 'Статья издержек'
		verbose_name_plural = 'Статьи издержек'
		ordering = ['name']

	def __str__(self):
		return self.name


class Expense(models.Model):
	# Конкретная операция расхода, которая попадет в отчет.
	category = models.ForeignKey(
		ExpenseCategory,
		on_delete=models.PROTECT,
		related_name='expenses',
		verbose_name='Статья издержек',
	)
	# Денежная величина издержки в валюте учета.
	amount = models.DecimalField(max_digits=12, decimal_places=2, verbose_name='Сумма')
	# Дата хозяйственной операции.
	expense_date = models.DateField(verbose_name='Дата операции')
	note = models.CharField(max_length=255, blank=True, verbose_name='Комментарий')

	class Meta:
		verbose_name = 'Издержка'
		verbose_name_plural = 'Издержки'
		ordering = ['-expense_date', 'id']

	def __str__(self):
		return f'{self.category.name}: {self.amount} ({self.expense_date})'

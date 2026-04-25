from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import PermissionRequiredMixin
from .models import Employee
from .forms import EmployeeForm

# 1. Просмотр списка сотрудников (Доступно всем, но объем данных зависит от авторизации)
class EmployeeListView(ListView):
    model = Employee
    template_name = 'employees/employee_list.html'
    context_object_name = 'employees'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Если пользователь не авторизован (Гость), мы передадим флаг в контекст
        # Этот флаг будет использоваться в HTML шаблоне для скрытия адреса и личного телефона
        context['is_guest'] = not self.request.user.is_authenticated
        return context

# 2. Добавление сотрудника (Доступно только Директору, т.к. только у него есть 'add_employee')
class EmployeeCreateView(PermissionRequiredMixin, CreateView):
    model = Employee
    form_class = EmployeeForm
    template_name = 'employees/employee_form.html'
    success_url = reverse_lazy('employee_list')
    permission_required = 'employees.add_employee'

# 3. Изменение сотрудника (Доступно Директору и Заместителю, т.к. у них есть 'change_employee')
class EmployeeUpdateView(PermissionRequiredMixin, UpdateView):
    model = Employee
    form_class = EmployeeForm
    template_name = 'employees/employee_form.html'
    success_url = reverse_lazy('employee_list')
    permission_required = 'employees.change_employee'

# 4. Удаление сотрудника (Доступно только Директору, т.к. у него есть 'delete_employee')
class EmployeeDeleteView(PermissionRequiredMixin, DeleteView):
    model = Employee
    template_name = 'employees/employee_confirm_delete.html'
    success_url = reverse_lazy('employee_list')
    permission_required = 'employees.delete_employee'

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User, Group, Permission
from django.contrib.contenttypes.models import ContentType
from employees.models import Employee

class Command(BaseCommand):
    help = 'Создает базовые группы, права, пользователей и начальные данные для системы сотрудников'

    def handle(self, *args, **options):
        self.stdout.write("Начинаем настройку ролей и пользователей...")

        # 1. Получаем тип контента для нашей модели Employee,
        # чтобы мы могли привязать к нему нужные права доступа.
        employee_ct = ContentType.objects.get_for_model(Employee)

        # 2. Получаем (из базы) стандартные права, которые Django автоматически создал для нашей модели
        view_perm = Permission.objects.get(codename='view_employee', content_type=employee_ct)
        add_perm = Permission.objects.get(codename='add_employee', content_type=employee_ct)
        change_perm = Permission.objects.get(codename='change_employee', content_type=employee_ct)
        delete_perm = Permission.objects.get(codename='delete_employee', content_type=employee_ct)

        # 3. Создаем группы (роли) и назначаем им соответствующие права
        # --- Группа "Directors" (Директора) ---
        # Имеют все возможные права
        director_group, _ = Group.objects.get_or_create(name='Directors')
        director_group.permissions.add(view_perm, add_perm, change_perm, delete_perm)

        # --- Группа "Deputies" (Заместители) ---
        # Имеют права только на просмотр и изменение (разрешены все действия, кроме удаления и добавления)
        deputy_group, _ = Group.objects.get_or_create(name='Deputies')
        deputy_group.permissions.add(view_perm, change_perm)

        # --- Группа "Secretaries" (Секретари) ---
        # Имеют права только на просмотр всех данных
        secretary_group, _ = Group.objects.get_or_create(name='Secretaries')
        secretary_group.permissions.add(view_perm)

        self.stdout.write("Группы и права доступа успешно созданы!")

        # 4. Создаем тестовых пользователей для каждой роли (если их еще нет)
        # Пользователь Директор
        if not User.objects.filter(username='director').exists():
            user = User.objects.create_user(username='director', password='password123', first_name='Иван', last_name='Директор')
            user.groups.add(director_group)
            self.stdout.write("Пользователь 'director' создан (пароль: password123)")

        # Пользователь Заместитель Директора
        if not User.objects.filter(username='deputy').exists():
            user = User.objects.create_user(username='deputy', password='password123', first_name='Петр', last_name='Заместитель')
            user.groups.add(deputy_group)
            self.stdout.write("Пользователь 'deputy' создан (пароль: password123)")

        # Пользователь Секретарь
        if not User.objects.filter(username='secretary').exists():
            user = User.objects.create_user(username='secretary', password='password123', first_name='Анна', last_name='Секретарь')
            user.groups.add(secretary_group)
            self.stdout.write("Пользователь 'secretary' создан (пароль: password123)")

        # 5. Добавляем немного тестовых данных (сотрудников)
        if not Employee.objects.exists():
            Employee.objects.create(
                last_name='Иванов', first_name='Иван', patronymic='Иванович',
                position='Менеджер по продажам', address='ул. Пушкина, д. 10',
                personal_phone='+7(999)123-45-67', work_phone='101'
            )
            Employee.objects.create(
                last_name='Петров', first_name='Сергей', patronymic='Васильевич',
                position='Системный администратор', address='ул. Ленина, д. 5',
                personal_phone='+7(900)000-11-22', work_phone='102'
            )
            Employee.objects.create(
                last_name='Смирнова', first_name='Ольга', patronymic='Николаевна',
                position='Бухгалтер', address='пр. Мира, д. 22',
                personal_phone='+7(926)555-44-33', work_phone='103'
            )
            Employee.objects.create(
                last_name='Сидоров', first_name='Алексей', patronymic='Петрович',
                position='Разработчик', address='ул. Чехова, д. 12',
                personal_phone='+7(916)777-88-99', work_phone='104'
            )
            self.stdout.write("В базу данных добавлено 4 тестовых сотрудника.")

        self.stdout.write(self.style.SUCCESS("Настройка успешно завершена!"))

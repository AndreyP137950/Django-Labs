# Подсказка: библиотеки, команды и логика работы

## 1) Основные библиотеки

### Внешняя библиотека
- Django 4.2: основной фреймворк для веб-приложения, ORM, маршрутизации, шаблонов, админ-панели.

### Стандартная библиотека Python
- decimal.Decimal: точные денежные расчеты без ошибок плавающей точки.

### Модули Django, используемые в проекте
- django.db.models: описание моделей базы данных.
- django.db.models.Sum: агрегирование сумм в запросах.
- django import forms: форма выбора периода и валидация дат.
- django.shortcuts.render: рендеринг HTML-страницы с контекстом.
- django.utils.timezone: получение текущей локальной даты.
- django.urls.path, include: маршруты проекта и приложения.
- django.contrib.admin: регистрация моделей для заполнения данных.

## 2) Основные команды

> Все команды запускать из папки проекта Laba10.

### Проверка Django
```powershell
C:/Users/andre/AppData/Local/Programs/Python/Python311/python.exe -m django --version
```

### Создание и применение миграций
```powershell
C:/Users/andre/AppData/Local/Programs/Python/Python311/python.exe manage.py makemigrations
C:/Users/andre/AppData/Local/Programs/Python/Python311/python.exe manage.py migrate
```

### Создание администратора
```powershell
C:/Users/andre/AppData/Local/Programs/Python/Python311/python.exe manage.py createsuperuser
```

### Запуск сервера
```powershell
C:/Users/andre/AppData/Local/Programs/Python/Python311/python.exe manage.py runserver
```

### Проверка проекта на ошибки конфигурации
```powershell
C:/Users/andre/AppData/Local/Programs/Python/Python311/python.exe manage.py check
```

## 3) Логика работы программы

### Шаг 1. Хранение данных
- В модели ExpenseCategory хранится справочник статей издержек.
- В модели Expense хранится каждая операция издержки:
  - статья,
  - сумма,
  - дата,
  - комментарий.

### Шаг 2. Ввод данных
- Операции и статьи заносятся через Django admin.
- Для этого модели зарегистрированы в admin.py.

### Шаг 3. Выбор периода отчета
- На главной странице есть форма с двумя датами:
  - дата начала,
  - дата окончания.
- Форма проверяет, что дата начала не позже даты окончания.

### Шаг 4. Построение отчета
- После отправки формы view-функция:
  - фильтрует записи Expense по диапазону дат,
  - группирует их по статье издержек,
  - считает сумму по каждой статье через Sum,
  - считает общий итог по всем статьям.

### Шаг 5. Отображение
- Шаблон report.html выводит таблицу:
  - статья издержек,
  - сумма по статье,
  - строка Итого.
- Если записей нет, показывается сообщение об отсутствии данных.

## 4) Структура проекта (кратко)
- laba10site/: настройки проекта и корневые маршруты.
- expenses/: модели, формы, представления и маршруты приложения отчета.
- templates/: HTML-шаблоны.
- static/css/: стили интерфейса.
- db.sqlite3: база данных SQLite.

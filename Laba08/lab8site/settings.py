"""Настройки Django-проекта Laba8.

Проект сделан как учебный сайт для печатной формы отчета по начислению
зарплаты сотрудникам.
"""

from pathlib import Path


# Базовая директория проекта, относительно которой задаются шаблоны,
# статические файлы и база данных.
BASE_DIR = Path(__file__).resolve().parent.parent

# Учебный секретный ключ; для реального проекта его нужно вынести в переменные среды.
SECRET_KEY = "django-insecure-laba8-salary-report-demo-key"

# Отладка включена для локальной разработки.
DEBUG = True

# Локальный запуск с типичными адресами разработки.
ALLOWED_HOSTS = ["localhost", "127.0.0.1"]

# Основные приложения Django и наше приложение с отчетами.
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "payroll",
]

# Стандартный middleware-слой Django.
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "lab8site.urls"

# Шаблоны хранятся в корневой папке templates и внутри приложения payroll.
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "lab8site.wsgi.application"

# База данных SQLite подходит для учебной лабораторной работы.
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

LANGUAGE_CODE = "ru-ru"
TIME_ZONE = "Europe/Moscow"
USE_I18N = True
USE_TZ = True

# Статические файлы: стили и простые служебные ресурсы.
STATIC_URL = "static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# После успешного входа пользователя возвращаем на главную страницу.
LOGIN_REDIRECT_URL = "/"
LOGOUT_REDIRECT_URL = "/"

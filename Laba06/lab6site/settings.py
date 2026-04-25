"""Настройки Django-проекта.

Здесь описываются подключенные приложения, база данных, шаблоны, статические
файлы и базовые параметры безопасности для учебного проекта.

Журнал изменений:
- DEV-AI01 | 2026-04-11 | Причина: детализация комментариев под требования ЛР6.
- Исходный фрагмент: не было комментария с фиксированной меткой изменения.
"""

from pathlib import Path


# Базовый каталог проекта, от которого строятся все относительные пути.
BASE_DIR = Path(__file__).resolve().parent.parent


# Ключ используется Django для служебных операций, связанных с безопасностью.
SECRET_KEY = "django-insecure-lab6-demo-key"


# В учебной среде удобно разрешить отладку, чтобы видеть ошибки и шаблоны.
DEBUG = True


# Для локального запуска этого достаточно; при публикации список нужно сузить.
ALLOWED_HOSTS = ["127.0.0.1", "localhost"]


# Подключаем стандартные модули Django и наше приложение с заметками.
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "journal",
]


# Определяем последовательность middleware, которая обрабатывает каждый запрос.
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]


# Главный файл маршрутов проекта.
ROOT_URLCONF = "lab6site.urls"


# Параметры шаблонов: Django ищет HTML-файлы в общей папке templates.
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]


# Точка входа для ASGI-сервера, если проект будут запускать асинхронно.
ASGI_APPLICATION = "lab6site.asgi.application"


# База данных SQLite подходит для лабораторной работы и не требует сервера.
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}


# Django использует эту функцию для проверки корректности паролей.
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Локализация под русскую среду и европейский формат времени.
LANGUAGE_CODE = "ru-ru"
TIME_ZONE = "Europe/Moscow"
USE_I18N = True
USE_TZ = True


# Статические файлы: CSS, изображения и другие ресурсы интерфейса.
STATIC_URL = "static/"
STATICFILES_DIRS = [BASE_DIR / "static"]


# Django 5 требует явного типа ключа по умолчанию для моделей.
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

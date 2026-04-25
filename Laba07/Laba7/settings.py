# Django параметры настройки проекта Laba7
# Основные параметры: язык, база данных, установленные приложения, middleware

import os
from pathlib import Path

# Базовая директория проекта
BASE_DIR = Path(__file__).resolve().parent.parent

# Секретный ключ для криптографии Django (для CSRF токенов, сессий и т.д.)
SECRET_KEY = 'django-insecure-test-key-for-lab-work-laba7-2024'

# Режим отладки (True для разработки, False для production)
DEBUG = True

# Список хостов, которым разрешено обслуживать приложение
ALLOWED_HOSTS = ['localhost', '127.0.0.1']

# Установленные приложения Django
# Включены основные приложения Django и наше локальное приложение assets
INSTALLED_APPS = [
    'django.contrib.admin',           # Админ-панель Django
    'django.contrib.auth',            # Система аутентификации
    'django.contrib.contenttypes',    # Система типов контента
    'django.contrib.sessions',        # Управление сессиями пользователей
    'django.contrib.messages',        # Система сообщений (уведомления)
    'django.contrib.staticfiles',     # Управление статическими файлами (CSS, JS, изображения)
    
    # Наше приложение для управления основными средствами
    'assets',
]

# Middleware - обработчики запросов/ответов
# Обрабатывают CSRF защиту, аутентификацию, сессии и т.д.
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# Основной URL конфигурационный файл
ROOT_URLCONF = 'Laba7.urls'

# Конфигурация шаблонов
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        # Директория где хранятся HTML шаблоны
        'DIRS': [BASE_DIR / 'templates'],
        # Поиск шаблонов в папке templates приложений
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# WSGI приложение (для развертывания на серверах)
WSGI_APPLICATION = 'Laba7.wsgi.application'

# Конфигурация базы данных
# Используется SQLite для простоты разработки
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        # Файл базы данных будет сохранен в корне проекта
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Валидация паролей - проверка надежности пароля
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Локализация - язык интерфейса
LANGUAGE_CODE = 'ru-ru'

# Временная зона
TIME_ZONE = 'Europe/Moscow'

# Включение интернационализации
USE_I18N = True

# Использование локальной информации (для форматирования дат, чисел)
USE_L10N = True

# Использование UTC для хранения времени в БД
USE_TZ = True

# Конфигурация статических файлов (CSS, JS, изображения)
# URL адрес статических файлов
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [BASE_DIR / 'static']

# Медиа файлы (загруженные пользователями файлы)
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Поле по умолчанию для первичного ключа
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

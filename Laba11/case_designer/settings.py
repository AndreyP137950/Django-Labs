"""
Настройки Django проекта case_designer

Проект: Лабораторная работа №11 - Мини Case система проектирования программ
Описание: Визуальное конструирование математических моделей с генерацией VBA кода
"""

import os
from pathlib import Path

# Базовый путь проекта
BASE_DIR = Path(__file__).resolve().parent.parent

# Секретный ключ (для разработки)
SECRET_KEY = 'django-insecure-case-designer-lab11-key'

# Режим отладки
DEBUG = True

# Допустимые хосты
ALLOWED_HOSTS = ['*']

# Установленные приложения
INSTALLED_APPS = [
    'django.contrib.contenttypes',
    'django.contrib.auth',
    'designer',
]

# Middleware
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.middleware.common.CommonMiddleware',
]

# Главный URL конфиг
ROOT_URLCONF = 'case_designer.urls'

# Конфигурация шаблонов
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'designer', 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
            ],
        },
    },
]

# База данных
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Статические файлы
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'designer', 'static'),
]

# Языковые параметры
LANGUAGE_CODE = 'ru-ru'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# ID типа основного ключа
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

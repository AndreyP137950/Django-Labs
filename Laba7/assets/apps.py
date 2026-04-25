# Django конфигурация приложения assets
# Определяет имя, описание и конфиги приложения

from django.apps import AppConfig

class AssetsConfig(AppConfig):
    # Тип поля по умолчанию для первичных ключей
    default_auto_field = 'django.db.models.BigAutoField'
    # Имя приложения
    name = 'assets'
    # Понятное имя приложения для админ-панели
    verbose_name = 'Управление основными средствами'

"""
ASGI конфигурация для проекта case_designer
"""
import os
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'case_designer.settings')
application = get_asgi_application()

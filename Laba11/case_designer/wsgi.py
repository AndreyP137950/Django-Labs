"""
WSGI конфигурация для проекта case_designer
"""
import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'case_designer.settings')
application = get_wsgi_application()

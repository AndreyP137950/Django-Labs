# Django главный URL маршрутизатор проекта Laba7
# Определяет основные маршруты и подключает маршруты приложений

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

# Корневые маршруты проекта.
urlpatterns = [
    # Админ-панель Django
    path('admin/', admin.site.urls),
    
    # Маршруты приложения assets (управление основными средствами)
    path('', include('assets.urls')),
]

# При DEBUG подключаем раздачу статических и медиа файлов.
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

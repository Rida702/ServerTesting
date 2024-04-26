# urls.py
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from .views import index_view

urlpatterns = [
    path("admin/", admin.site.urls),
    path('', include('imageApp.urls')),
    path('', index_view, name='index'),  # Include the index view URL pattern
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

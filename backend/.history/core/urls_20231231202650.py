from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from imageApp.views import index_view
from .views import upload_image

urlpatterns = [
    path("admin/", admin.site.urls),
    path('upload/', upload_image, name='upload_image'),
    path('', include('imageApp.urls')),
    path('', index_view, name='index'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

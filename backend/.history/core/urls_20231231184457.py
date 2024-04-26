from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path("admin/", admin.site.urls),
    path('', index_view, name=''),
    path('imageApp/', include('imageApp.urls')),
]

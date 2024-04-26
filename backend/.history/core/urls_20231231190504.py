from django.contrib import admin
from django.urls import path,include
from imageApp.views import index_view

urlpatterns = [
    path("admin/", admin.site.urls),
    path('imageApp/', include('imageApp.urls')),
]

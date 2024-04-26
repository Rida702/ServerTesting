from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path("admin/", admin.site.urls),
    path('imageApp/', include('your_app_name.urls')),
]

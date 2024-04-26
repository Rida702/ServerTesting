# urls.py
from django.urls import path,include
from .views import upload_image


urlpatterns = [
    path('', upload_image, name='upload_image'),
    path('api/', include('imageApp.api.urls')),
]

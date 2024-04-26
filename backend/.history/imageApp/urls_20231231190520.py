# urls.py
from django.urls import path
from .views import upload_image
from imageApp.views import index_view

urlpatterns = [
    path('upload/', upload_image, name='upload_image'),
    path('', index_view, name='index'),
]

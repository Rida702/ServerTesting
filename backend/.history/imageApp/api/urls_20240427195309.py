from django.urls import path, include
from imageApp.views import ImageUploadView, ResultImageView
from rest_framework import routers
from .views import ImageViewSet

router = routers.DefaultRouter()
router.register(r'images', ImageViewSet)

urlpatterns = [
    path('',include(router.urls)),
    path('uploadWristImage/', ImageUploadView , name='wrist_upload_image'),  # Endpoint for uploading images
    path('watchResult/', ResultImageView , name='watch_result_image'),  # Endpoint for retrieving result images
    path('uploaf/', views.hello_world, name='hello_world'),
]

from django.urls import path, include
from imageApp.views import ImageUploadView, ResultImageView, hello_world, UploadImages
from rest_framework import routers
from .views import ImageViewSet

router = routers.DefaultRouter()
router.register(r'images', ImageViewSet)
router.register(r'uploadimages', UploadImages)


print('API URL')
urlpatterns = [
    path('',include(router.urls)),
    #path('uploadWristImage/', ImageUploadView , name='wrist_upload_image'),  # Endpoint for uploading images
    path('watchResult/', ResultImageView , name='watch_result_image'),  # Endpoint for retrieving result images
    path('uploadText/', hello_world, name='hello_world'),
]

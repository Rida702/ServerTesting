from django.urls import path, include
#from imageApp.views import ImageUploadView, ResultImageView, hello_world, UploadImages
from imageApp.views import hello_world, UploadImages
from rest_framework import routers
from .views import ImageViewSet
from imageApp.views import UploadImages


router = routers.DefaultRouter()
router.register(r'images', ImageViewSet)
#router.register(r'uploadimages', UploadImages)


print('API URL')
urlpatterns = [
    path('',include(router.urls)),
    path('uploadWristImage/', UploadImages , name='wrist_upload_image'),
    path('uploadText/', hello_world, name='hello_world'),
]

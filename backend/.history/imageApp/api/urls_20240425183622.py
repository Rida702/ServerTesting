from django.urls import path
from imageApp.views import ImageUploadView, ResultImageView

router = routers.DefaultRouter()
router.register(r'events', ImageViewSet)

urlpatterns = [
    path('uploadWristImage/', ImageUploadView , name='wrist_upload_image'),  # Endpoint for uploading images
    path('watchResult/', ResultImageView , name='watch_result_image'),  # Endpoint for retrieving result images
]

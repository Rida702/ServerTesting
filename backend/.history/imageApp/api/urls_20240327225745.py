from django.urls import path
from .views import ImageUploadView, ResultImageView

urlpatterns = [
    path('uploadWristImage/', ImageUploadView.as_view(), name='wrist_upload_image'),  # Endpoint for uploading images
    path('atchresultImage/<int:image_id>/', ResultImageView.as_view(), name='watch_result_image'),  # Endpoint for retrieving result images
]

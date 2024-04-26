from django.urls import path
from imageApp.views import ImageUploadView, ResultImageView

urlpatterns = [
    path('uploadWristImage/', ImageUploadView, name='wrist_upload_image'),  # Endpoint for uploading images
    path('watchResult/<int:image_id>/', ResultImageView.as_view(), name='watch_result_image'),  # Endpoint for retrieving result images
]

from django.urls import path
from .views import ImageUploadView, ResultImageView

urlpatterns = [
    path('uploadImage/', ImageUploadView.as_view(), name='upload_image'),  # Endpoint for uploading images
    path('resultImage/<int:image_id>/', ResultImageView.as_view(), name='result_image'),  # Endpoint for retrieving result images
]

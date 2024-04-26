from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .forms import ImageUploadForm
from .models import ImageModel
from django.conf import settings
from imageApp.model.image_processing import detect_wrist, overlay_watch
from django.shortcuts import render
from django.core.files.base import ContentFile
from PIL import Image
from io import BytesIO
import os
from api import ImageModelSerializer 
from api.serializers import ImageModelSerializer

class ImageUploadView(APIView):
    def post(self, request, *args, **kwargs):
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            watch_image = request.FILES['watch_image']
            wrist_image = request.FILES['wrist_image']

            # Paths where images are stored
            watch_image_path = f"uploaded_images/{watch_image.name}"
            wrist_image_path = f"uploaded_images/{wrist_image.name}"

            try:
                # Save the images
                with open(os.path.join(settings.MEDIA_ROOT, watch_image_path), 'wb') as watch_file:
                    watch_file.write(watch_image.read())

                with open(os.path.join(settings.MEDIA_ROOT, wrist_image_path), 'wb') as wrist_file:
                    wrist_file.write(wrist_image.read())

                # Detect wrist
                wrist_box = detect_wrist(os.path.join(settings.MEDIA_ROOT, wrist_image_path))

                # Overlay watch on wrist
                result_image_name = f"result_images/result_{watch_image.name}"
                result_image_path, result_image = overlay_watch(wrist_box, os.path.join(settings.MEDIA_ROOT, wrist_image_path), os.path.join(settings.MEDIA_ROOT, watch_image_path), os.path.join(settings.MEDIA_ROOT, result_image_name))

                # Save the result image
                result_image_path = os.path.join(settings.MEDIA_ROOT, 'result_images', result_image_name)
                result_pil_image = Image.fromarray(result_image.astype('uint8'))
                result_pil_image.save(result_image_path)

                # Save image paths to the database
                image_model = ImageModel.objects.create(
                    watch_image=watch_image,
                    wrist_image=wrist_image,
                    result_image=result_image_name
                )

                # Prepare URLs for the template
                context = {
                    'watch_image_url': image_model.watch_image.url,
                    'wrist_image_url': image_model.wrist_image.url,
                    'result_image_url': image_model.result_image.url,
                }
                print(f"Result Image Path: {result_image_name}")

                return render(request, 'result.html', context)

            except Exception as e:
                print(f"Error during image processing: {e}")
                # Handle the error gracefully, provide feedback to the user, etc.

        return Response({'error': 'Invalid form data'}, status=status.HTTP_400_BAD_REQUEST)

class ResultImageView(APIView):
    def get(self, request, image_id, *args, **kwargs):
        try:
            image_model = ImageModel.objects.get(id=image_id)
        except ImageModel.DoesNotExist:
            return Response({'error': 'Image not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = ImageModelSerializer(image_model)

        return Response(serializer.data)

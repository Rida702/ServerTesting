from rest_framework import viewsets, status
from rest_framework.response import Response
from models import ImageModel
from .serializers import ImageModelSerializer
from .forms import ImageUploadForm  # Import your ImageUploadForm if needed
from django.conf import settings
from imageApp.model.image_processing import detect_wrist, overlay_watch
from PIL import Image
import os

class ImageViewSet(viewsets.ViewSet):
    def create(self, request):
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

                serializer = ImageModelSerializer(image_model)

                return Response(serializer.data, status=status.HTTP_201_CREATED)

            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({'error': 'Invalid form data'}, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        try:
            image_model = ImageModel.objects.get(pk=pk)
            serializer = ImageModelSerializer(image_model)
            return Response(serializer.data)
        except ImageModel.DoesNotExist:
            return Response({'error': 'Image not found'}, status=status.HTTP_404_NOT_FOUND)

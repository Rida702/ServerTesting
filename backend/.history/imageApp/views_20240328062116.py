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
from imageApp.api.serializers import ImageModelSerializer
from django.http import request
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def ImageUploadView(request):
    if request.method == 'POST':
        # Assuming wrist_image and watch_image are sent as files
        watch_image = request.FILES.get('watch_image')
        wrist_image = request.FILES.get('wrist_image')

        if watch_image and wrist_image:
            # Paths where images will be stored
            watch_image_path = os.path.join(settings.MEDIA_ROOT, f"uploaded_images/{watch_image.name}")
            wrist_image_path = os.path.join(settings.MEDIA_ROOT, f"uploaded_images/{wrist_image.name}")

            try:
                # Save the images
                with open(watch_image_path, 'wb') as watch_file:
                    for chunk in watch_image.chunks():
                        watch_file.write(chunk)

                with open(wrist_image_path, 'wb') as wrist_file:
                    for chunk in wrist_image.chunks():
                        wrist_file.write(chunk)

                # Detect wrist
                wrist_box = detect_wrist(wrist_image_path)

                # Overlay watch on wrist
                result_image_name = f"result_images/result_{watch_image.name}"
                result_image_path, result_image = overlay_watch(wrist_box, wrist_image_path, watch_image_path)

                # Save the result image
                result_image_path = os.path.join(settings.MEDIA_ROOT, result_image_name)
                result_pil_image = Image.fromarray(result_image.astype('uint8'))
                result_pil_image.save(result_image_path)

                # Save image paths to the database
                my_model_instance = ImageModel.objects.create(
                    watch_image=result_image_path,  # Save result image path instead of watch_image path
                    wrist_image=wrist_image_path,
                    result_image=result_image_path
                )

                # Prepare URLs for the response
                context = {
                    'watch_image_url': my_model_instance.watch_image.url,
                    'wrist_image_url': my_model_instance.wrist_image.url,
                    'result_image_url': my_model_instance.result_image.url,
                }

                return JsonResponse(context)

            except Exception as e:
                print(f"Error during image processing: {e}")
                return JsonResponse({'error': 'Error during image processing'}, status=500)

    return JsonResponse({'error': 'Invalid request'}, status=400)

class ResultImageView(APIView):
    def get(self, request, image_id, *args, **kwargs):
        try:
            image_model = ImageModel.objects.get(id=image_id)
        except ImageModel.DoesNotExist:
            return Response({'error': 'Image not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = ImageModelSerializer(image_model)

        return Response(serializer.data)

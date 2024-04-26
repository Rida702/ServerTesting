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
from django.http import JsonResponse

@csrf_exempt
def ImageUploadView(request):
    if request.method == 'POST':
        # Assuming wrist_image and watch_image are sent as files
        print(request.FILES)
        watch_image = request.FILES.get('watchImage')
        wrist_image = request.FILES.get('wristImage')
        
        if watch_image is None or wrist_image is None:
            return JsonResponse({'error': 'Both watchImage and wristImage must be provided'}, status=400)
        if watch_image is None:
            print("Watch Image is None")
        if wrist_image is None:
            print("Wrist Image Path")

        # Paths where images are stored
        watch_image_path = f"uploaded_images/{watch_image.name}"
        wrist_image_path = f"uploaded_images/{wrist_image.name}"

        print(f"Watch Image Path: {watch_image_path}")
        print(f"Wrist Image Path: {wrist_image_path}")

        try:
            # Save the images
            with open(os.path.join(settings.MEDIA_ROOT, watch_image_path), 'wb') as watch_file:
                watch_file.write(watch_image.read())

            with open(os.path.join(settings.MEDIA_ROOT, wrist_image_path), 'wb') as wrist_file:
                wrist_file.write(wrist_image.read())

            # Detect wrist
            wrist_box = detect_wrist(os.path.join(settings.MEDIA_ROOT, wrist_image_path))
            print(f"Wrist Box: {wrist_box}")


            # Overlay watch on wrist
            result_image_name = f"result_images/result_{watch_image.name}"
            result_image_path, result_image = overlay_watch(wrist_box, os.path.join(settings.MEDIA_ROOT, wrist_image_path), os.path.join(settings.MEDIA_ROOT, watch_image_path), os.path.join(settings.MEDIA_ROOT, result_image_name))

            print("FILE NOT READ, 500")
            # Assuming result_image is your NumPy array
            result_pil_image = Image.fromarray(result_image.astype('uint8'))
            
            # Save the PIL Image to a BytesIO buffer
            image_io = BytesIO()
            result_pil_image.save(image_io, format='JPEG')
            image_io.seek(0)
            
            # Save paths to the database
            my_model_instance = ImageModel()

            # Save watch image
            my_model_instance.watch_image = request.FILES['watch_image']
            my_model_instance.watch_image.name = watch_image_path
            my_model_instance.save()

            # Save wrist image
            my_model_instance.wrist_image = request.FILES['wrist_image']
            my_model_instance.wrist_image.name = wrist_image_path
            my_model_instance.save()
            
            # Save result image
            my_model_instance.result_image.name = result_image_name
            my_model_instance.result_image.save(result_image_name, ContentFile(image_io.read()), save=True)


            # Prepare URLs for the template
            context = {
                'watch_image_url': my_model_instance.watch_image.url,
                'wrist_image_url': my_model_instance.wrist_image.url,
                'result_image_url': my_model_instance.result_image.url,
            }
            print(f"Result Image Path: {{result_image_url}}")
            
            return JsonResponse(context)

        except Exception as e:
            print(f"Error during image processing: {e}")
            return JsonResponse({'error': 'Error during image processing'}, status=500)

    return JsonResponse({'error': 'Invalid request'}, status=400)

def ResultImageView(request):
    if request.method == 'GET':
        # Retrieve the latest ImageModel instance from the database
        latest_image = ImageModel.objects.last()

        # Check if the latest_image exists
        if latest_image is not None:
            # Prepare the context with the URL of the result image
            context = {
                'result_image_url': latest_image.result_image.url
            }
            return JsonResponse(context)
        else:
            return JsonResponse({'error': 'No result image found'}, status=404)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)
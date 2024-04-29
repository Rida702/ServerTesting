import os
import requests
from django.conf import settings
from django.http import JsonResponse
from .models import ImageModel
from imageApp.model.image_processing import detect_wrist, overlay_watch
from PIL import Image
from io import BytesIO


def ImageUploadView(request):
    if request.method == 'POST':
        # Extract image URLs from the request data
        watch_image_url = request.POST.get('watchImage')
        wrist_image_url = request.POST.get('wristImage')
        
        if not watch_image_url or not wrist_image_url:
            return JsonResponse({'error': 'Both watchImage and wristImage URLs must be provided'}, status=400)

        try:
            # Download images from URLs
            watch_image_response = requests.get(watch_image_url)
            wrist_image_response = requests.get(wrist_image_url)
            
            # Check if images were downloaded successfully
            if watch_image_response.status_code != 200 or wrist_image_response.status_code != 200:
                return JsonResponse({'error': 'Failed to download one or more images'}, status=400)
            
            # Convert image content to PIL Image objects
            watch_image = Image.open(BytesIO(watch_image_response.content))
            wrist_image = Image.open(BytesIO(wrist_image_response.content))

            # Perform image processing
            wrist_box = detect_wrist(wrist_image)
            result_image = overlay_watch(wrist_box, wrist_image, watch_image)

            # Save result image
            result_image_name = f"result_images/result_{os.path.basename(watch_image_url)}"
            result_image_path = os.path.join(settings.MEDIA_ROOT, result_image_name)
            result_image.save(result_image_path)

            # Save paths to the database
            my_model_instance = ImageModel.objects.create(
                watch_image_url=watch_image_url,
                wrist_image_url=wrist_image_url,
                result_image=result_image_name
            )

            # Prepare URLs for the response
            context = {
                'watch_image_url': watch_image_url,
                'wrist_image_url': wrist_image_url,
                'result_image_url': result_image_path,
            }
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

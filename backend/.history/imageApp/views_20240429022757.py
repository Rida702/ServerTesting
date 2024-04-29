from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import ImageModel
from imageApp.model.image_processing import detect_wrist, overlay_watch
from django.core.files.base import ContentFile
from PIL import Image
import os
import base64
from io import BytesIO
from django.http import HttpRequest
from urllib.parse import urljoin

print('VIEW')

@csrf_exempt
def hello_world(request):
    print('Here 1')
    if request.method == 'POST':
        print('Here')
        data = json.loads(request.body)
        message = data.get('message', 'Hello')
        print('Received message:', message)  # Print the received message
        return JsonResponse({'response': message + ' from Django!'})
    else:
        return JsonResponse({'error': 'Only POST requests are allowed'})

class UploadImages(APIView):
    def post(self, request: HttpRequest):
        try:
            wrist_image_data = request.data.get('wristImage')
            watch_image_data = request.data.get('watchImage')

            # Decode base64 image data
            wrist_image_decoded = base64.b64decode(wrist_image_data.split(',')[1])
            watch_image_decoded = base64.b64decode(watch_image_data.split(',')[1])

            # Save images to a directory
            wrist_image_path = os.path.join('media', 'wrist_image.jpg')
            watch_image_path = os.path.join('media', 'watch_image.jpg')                      
            base_url = request.build_absolute_uri('/')  
            
            
            wrist_image_url = urljoin(base_url, wrist_image_path)
            watch_image_url = urljoin(base_url, watch_image_path)
            
            with open(wrist_image_path, 'wb') as wrist_image_file:
                wrist_image_file.write(wrist_image_decoded)

            with open(watch_image_path, 'wb') as watch_image_file:
                watch_image_file.write(watch_image_decoded)

            # Assuming detect_wrist and overlay_watch functions exist
            wrist_box = detect_wrist(wrist_image_path)
            result_image_name = f"result_images/result_{watch_image_path.split('/')[-1]}"
            result_image_path, result_image = overlay_watch(wrist_box, wrist_image_path, watch_image_path, result_image_name)

            # Saving the result image
            result_pil_image = Image.fromarray(result_image.astype('uint8'))
            result_image_path = os.path.join('media', 'result_image.jpg')
            result_image_url = urljoin(base_url, result_image_path)
            result_image_io = BytesIO()
            result_pil_image.save(result_image_io, format='JPEG')
            
            with open(result_image_path, 'wb') as result_image_file:
                result_image_file.write(result_image_io.read())

            my_model_instance = ImageModel(watch_image=wrist_image_decoded,wrist_image=wrist_image_decoded)
            my_model_instance.save()
            
            context = {
                'wrist_url': wrist_image_url,
                'watch_url': watch_image_url,
                'result_url': result_image_url
            }

            return Response(context, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
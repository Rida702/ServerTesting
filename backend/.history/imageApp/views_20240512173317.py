from django.http import JsonResponse
import json
from imageApp.model.image_processing import detect_wrist, overlay_watch, preProcessWatchImage
import os
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from PIL import Image as PILImage
from io import BytesIO
import cv2

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
    
def get_image_dimensions(image):
    # Load image using PIL
    image_data = BytesIO(image.read())
    pil_image = PILImage.open(image_data)
    
    # Get dimensions
    dimensions = pil_image.size
    
    return dimensions

@csrf_exempt
def UploadImages(request):
    if request.method == 'POST':
        print("Inside iamge upload")
        try:
            print("A")
            if 'wristImage' in request.FILES and 'watchImage' in request.FILES:
                wrist_image = request.FILES['wristImage']
                watch_image = request.FILES['watchImage']
                
                # Get dimensions of wrist image
                wrist_image_dimensions = get_image_dimensions(wrist_image)
                print("Wrist image dimensions:", wrist_image_dimensions)
                
                # Get dimensions of watch image
                watch_image_dimensions = get_image_dimensions(watch_image)
                print("Watch image dimensions:", watch_image_dimensions)
                
                # Save images to media directory
                print("B")
                wrist_image_path = os.path.join(settings.MEDIA_ROOT, 'wrist_image.jpg')
                watch_image_path = os.path.join(settings.MEDIA_ROOT, 'watch_image.jpg')
                
                print("C")
                with open(wrist_image_path, 'wb') as wrist_image_file:
                    for chunk in wrist_image.chunks():
                        wrist_image_file.write(chunk)
                print("D")
                with open(watch_image_path, 'wb') as watch_image_file:
                    for chunk in watch_image.chunks():
                        watch_image_file.write(chunk)
                
                print("E")
                # Assuming detect_wrist and overlay_watch functions exist
                watch_bg = preProcessWatchImage(watch_image_path)
                print("E1")
                wrist_img = cv2.imread(wrist_image_path)
                wrist_box = detect_wrist(wrist_img)
                print("E2")
                result_image_name = f"result_images/result_{watch_image_path.split('/')[-1]}"
                print("E3")
                result_image = overlay_watch(wrist_box, wrist_image_path, watch_bg)
                
                print("F")
                # Save result image
                result_image_path = os.path.join(settings.MEDIA_ROOT, 'result_image.jpg')
                cv2.imwrite(result_image_path, result_image)
                
                # Construct URLs for saved images
                print("G")
                base_url = request.build_absolute_uri('/')  
                wrist_image_url = os.path.join(base_url, 'media', 'wrist_image.jpg')
                watch_image_url = os.path.join(base_url, 'media', 'watch_image.jpg')
                result_image_url = os.path.join(base_url, 'media', 'result_image.jpg')
                
                print("H")
                
                #Saving to database
                
                
                context = {
                    'wrist_url': wrist_image_url,
                    'watch_url': watch_image_url,
                    'result_url': result_image_url
                }
                
                print("I")
                return JsonResponse(context, status=200)
            else:
                return JsonResponse({'error': 'wristImage and watchImage files are required'}, status=400)
                
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
                
    else:
        return JsonResponse({'error': 'Only POST requests are allowed'}, status=405)


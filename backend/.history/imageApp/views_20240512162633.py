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
                wrist_box = detect_wrist(wrist_image_path)
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

    
    
"""class UploadImages(APIView):
    def post(self, request: HttpRequest):
        print("HERE 12")
        try:
            print("A")
            wrist_image = request.FILES['wristImage']
            watch_image = request.FILES['watchImage']
            print("B")
            # Save images to a directory
            wrist_image_path = os.path.join('media', 'wrist_image.jpg')
            watch_image_path = os.path.join('media', 'watch_image.jpg')
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
            wrist_box = detect_wrist(wrist_image_path)
            result_image_name = f"result_images/result_{watch_image_path.split('/')[-1]}"
            result_image_path, result_image = overlay_watch(wrist_box, wrist_image_path, watch_image_path, result_image_name)
            print("F")
            # Save result image
            result_image_path = os.path.join('media', 'result_image.jpg')
            result_image.save(result_image_path)
            print("G")
            # Return URLs of saved images
            base_url = request.build_absolute_uri('/')  
            wrist_image_url = os.path.join(base_url, wrist_image_path)
            watch_image_url = os.path.join(base_url, watch_image_path)
            result_image_url = os.path.join(base_url, result_image_path)
            print("H")
            context = {
                'wrist_url': wrist_image_url,
                'watch_url': watch_image_url,
                'result_url': result_image_url
            }
            print("Ii")
            return Response("POST request received", status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST) """
            

"""class UploadImages(APIView):
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
            print("1")

            # Assuming detect_wrist and overlay_watch functions exist
            wrist_box = detect_wrist(wrist_image_path)
            print("2")
            result_image_name = f"result_images/result_{watch_image_path.split('/')[-1]}"
            print("3")
            result_image_path, result_image = overlay_watch(wrist_box, wrist_image_path, watch_image_path, result_image_name)

            # Saving the result image
            print("4")
            result_pil_image = Image.fromarray(result_image.astype('uint8'))
            result_image_path = os.path.join('media', 'result_image.jpg')
            result_image_url = urljoin(base_url, result_image_path)
            result_image_io = BytesIO()
            result_pil_image.save(result_image_io, format='JPEG')
            print("112")
            
            with open(result_image_path, 'wb') as result_image_file:
                result_image_file.write(result_image_io.read())
            print("11")
            
            # Saving the images to the model instance
            my_model_instance = ImageModel()

            # Save watch image
            watch_image_name = 'watch_image.jpg'
            watch_image_content = ContentFile(watch_image_decoded)
            my_model_instance.watch_image.save(watch_image_name, watch_image_content, save=True)

            # Save wrist image
            wrist_image_name = 'wrist_image.jpg'
            wrist_image_content = ContentFile(wrist_image_decoded)
            my_model_instance.wrist_image.save(wrist_image_name, wrist_image_content, save=True)
            
            result_image_name = 'result_image.jpg'
            result_image_content = ContentFile(result_image_io.read(), name=result_image_name)
            my_model_instance.result_image.save(result_image_name, result_image_content, save=True)
            
            my_model_instance.save()
            
            context = {
                'wrist_url': wrist_image_url,
                'watch_url': watch_image_url,
                'result_url': result_image_url
            }

            return Response(context, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
"""


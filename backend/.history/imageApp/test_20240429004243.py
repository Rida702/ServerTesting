from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
import os
import base64
from PIL import Image
from io import BytesIO
from .models import ImageModel

class UploadImages(APIView):
    def post(self, request):
        try:
            
            wrist_image_data = request.data.get('wristImage')
            watch_image_data = request.data.get('watchImage')

            # Decode base64 image data
            wrist_image_decoded = base64.b64decode(wrist_image_data.split(',')[1])
            watch_image_decoded = base64.b64decode(watch_image_data.split(',')[1])

            # Save images to a directory
            wrist_image_path = os.path.join('media', 'wrist_image.jpg')
            watch_image_path = os.path.join('media', 'watch_image.jpg')

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
            result_image_io = BytesIO()
            result_pil_image.save(result_image_io, format='JPEG')

            # Save the images to the model
            my_model_instance = ImageModel.objects.create(watchImage=watch_image_data, wristImage=wrist_image_data, result_image=result_image_io.getvalue())

            context = {
                'watch_image_url': my_model_instance.watchImage.url,
                'wrist_image_url': my_model_instance.wristImage.url,
                'result_image_url': my_model_instance.result_image.url,
            }

            return Response(context, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

from django.urls import path, include
from imageApp.views import ImageUploadView, ResultImageView
from rest_framework import routers
from .views import ImageViewSet

router = routers.DefaultRouter()
router.register(r'images', ImageViewSet)

urlpatterns = [
    path('',include(router.urls)),
    path('uploadWristImage/', ImageUploadView , name='wrist_upload_image'),  # Endpoint for uploading images
    path('watchResult/', ResultImageView , name='watch_result_image'),  # Endpoint for retrieving result images
    from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

@csrf_exempt
def hello_world(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        message = data.get('message', 'Hello')
        return JsonResponse({'response': message + ' from Django!'})
    else:
        return JsonResponse({'error': 'Only POST requests are allowed'})

]

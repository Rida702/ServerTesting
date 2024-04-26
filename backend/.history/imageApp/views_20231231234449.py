# views.py
from django.shortcuts import render
from .forms import ImageUploadForm
from PIL import Image
import os
from django.conf import settings
from django.core.files import File

def index_view(request):
    return render(request, 'index.html')

def upload_view(request):
    return render(request, 'upload.html')


def grayscale_image(image_path):
    img = Image.open(image_path).convert('L')
    save_path = os.path.join('media', 'grayscaled')
    print(save_path)
    #save_path = os.path.join(settings.MEDIA_ROOT, 'grayscaled')
    os.makedirs(save_path, exist_ok=True)
    grayscale_filename = f"grayscaled_{os.path.basename(image_path)}"
    grayscale_path = os.path.join(save_path, grayscale_filename)

    # Use Django's File class to handle file saving
    with open(grayscale_path, 'wb') as f:
        img.save(f, format="JPEG")

    return grayscale_path

def upload_image(request):
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_image = form.save()
            

            grayscale_path = grayscale_image(uploaded_image.image.path)

            # Construct the relative path manually
            relative_path = os.path.relpath(grayscale_path, settings.MEDIA_ROOT)

            relative_path = relative_path.lstrip('/')

            uploaded_image.grayscale_image = f'media/{relative_path}'
            uploaded_image.save()
            return render(request, 'result.html', {'uploaded_image': uploaded_image})
    else:
        form = ImageUploadForm()
    return render(request, 'upload.html', {'form': form})

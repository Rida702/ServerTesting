# views.py
from django.shortcuts import render
from .forms import ImageUploadForm
from PIL import Image
import os
from django.conf import settings
from django.core.files import File
import time

def index_view(request):
    return render(request, 'index.html')

def upload_view(request):
    return render(request, 'upload.html')

def grayscale_image(image_path):
    img = Image.open(image_path).convert('L')
    save_path = os.path.join(settings.MEDIA_ROOT, 'grayscaled')
    os.makedirs(save_path, exist_ok=True)
    grayscale_filename = f"grayscaled_{os.path.basename(image_path)}"
    grayscale_path = os.path.join(save_path, grayscale_filename)

    with open(grayscale_path, 'wb') as f:
        img.save(f, format="JPEG")
    return grayscale_path

"""def upload_image(request):
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            #commit=False
            uploaded_image = form.save(commit=False)
            
            grayscale_path = grayscale_image(uploaded_image.image.path)

            relative_path = os.path.relpath(grayscale_path, settings.MEDIA_ROOT)
            relative_path = relative_path.lstrip('/')

            uploaded_image.grayscale_image = f'media/{relative_path}'
            uploaded_image.save()

            filename = os.path.basename(uploaded_image.image.path)
            grayscale_image_url = f'/media/grayscaled/grayscaled_{filename}'
            print("This is Image path", grayscale_image_url)

            context = {
                'uploaded_image': uploaded_image,
                'grayscale_image_url': grayscale_image_url,
            }
            return render(request, 'result.html', context)
    else:
        form = ImageUploadForm()

    return render(request, 'upload.html', {'form': form})"""
def upload_image(request):
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_image = form.save(commit=False)

            grayscale_path = grayscale_image(uploaded_image.image.path)

            original_image_filename = os.path.basename(uploaded_image.image.path)
            uploaded_image.image.save(original_image_filename, File(open(uploaded_image.image.path, 'rb')))
            print("Original Image Path:", f'media/uploads/{original_image_filename}')
            
            original_image_path = f'media/uploads/{original_image_filename}'

            uploaded_image.grayscale_image = f'media/grayscaled/grayscaled_{original_image_filename}'

            uploaded_image.save()
            time.sleep(5)
            
            print("Grayscale Image Path:", uploaded_image.grayscale_image)

            filename = original_image_filename
            grayscale_image_url = uploaded_image.grayscale_image

            context = {
                'uploaded_image_url': original_image_path,
                'grayscale_image_url': grayscale_image_url,
            }

            return render(request, 'result.html', context)
    else:
        form = ImageUploadForm()

    return render(request, 'upload.html', {'form': form})
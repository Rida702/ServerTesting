# views.py
from django.shortcuts import render
from .forms import ImageUploadForm
from PIL import Image
import os
from django.conf import settings

def index_view(request):
    return render(request, 'index.html')

def upload_view(request):
    return render(request, 'upload.html')

def grayscale_image(image_path):
    img = Image.open(image_path).convert('L')
    save_path = os.path.join('greyscaled')  # Remove 'media' from here
    os.makedirs(save_path, exist_ok=True)
    grayscale_filename = f"greyscaled_{os.path.basename(image_path)}"
    grayscale_path = os.path.join(save_path, grayscale_filename)
    img.save(grayscale_path, format="JPEG")
    return grayscale_path

def upload_image(request):
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_image = form.save()

            grayscale_path = grayscale_image(uploaded_image.image.path)
            print(f"Original Image Path: {uploaded_image.image.path}")
            print(f"Grayscale Image Path: {grayscale_path}")

            # Remove 'media' from the beginning of the path
            uploaded_image.grayscale_image = os.path.relpath(grayscale_path, settings.MEDIA_ROOT)
            uploaded_image.save()

            return render(request, 'result.html', {'uploaded_image': uploaded_image})
    else:
        form = ImageUploadForm()
    return render(request, 'upload.html', {'form': form})

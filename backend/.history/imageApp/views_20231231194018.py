# views.py
from django.shortcuts import render, redirect
from .forms import ImageUploadForm
from PIL import Image
from io import BytesIO
import base64
from django.shortcuts import render
import os

def index_view(request):
    return render(request, 'index.html')

def upload_view(request):
    return render(request, 'upload.html')

def grayscale_image(image_path, save_path):
    img = Image.open(image_path).convert('L')
    grayscale_path = os.path.join(save_path, f"greyscaled_{os.path.basename(image_path)}")
    img.save(grayscale_path, format="JPEG")
    return grayscale_path

def upload_image(request):
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_image = form.save()

            save_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'media', 'greyscaled')
            os.makedirs(save_path, exist_ok=True)

            grayscale_filename = f"greyscaled_{os.path.basename(uploaded_image.image.path)}"
            grayscale_path = os.path.join(save_path, grayscale_filename)

            grayscale_data = grayscale_image(uploaded_image.image.path, grayscale_path)

            uploaded_image.grayscale_image = f'media/greyscaled/{grayscale_filename}'
            uploaded_image.save()

            return render(request, 'result.html', {'uploaded_image': uploaded_image})
    else:
        form = ImageUploadForm()
    return render(request, 'upload.html', {'form': form})



# views.py
from io import BytesIO
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

"""def grayscale_image(image_path):
    img = Image.open(image_path).convert('L')
    save_path = os.path.join(settings.MEDIA_ROOT, 'grayscaled')
    os.makedirs(save_path, exist_ok=True)
    grayscale_filename = f"grayscaled_{os.path.basename(image_path)}"
    grayscale_path = os.path.join(save_path, grayscale_filename)

    with open(grayscale_path, 'wb') as f:
        img.save(f, format="JPEG")
    return grayscale_path"""
    
def grayscale_image(image_path):
    img = Image.open(image_path).convert('L')

    # Create a BytesIO object to hold the grayscale image in memory
    with BytesIO() as f:
        img.save(f, format="JPEG")
        f.seek(0)
        # Return the grayscale image as a BytesIO object
        return f


def upload_image(request):
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_image = form.save(commit=False)
            
            filename = os.path.basename(uploaded_image.image.path)
            uploaded_image.grayscale_image = f'/media/uploads/{filename}'
            original_image_url = f'/media/uploads/{filename}'

            filename = os.path.basename(uploaded_image.image.path)
            grayscale_image_url = f'/media/grayscaled/grayscaled_{filename}'
            print("This is Image path", grayscale_image_url)
            
            uploaded_image.save()

            context = {
                'original_image_url': original_image_url,
                'grayscale_image_url': grayscale_image_url,
            }
            return render(request, 'result.html', context)
    else:
        form = ImageUploadForm()

    return render(request, 'upload.html', {'form': form})
# views.py
from io import BytesIO
from django.shortcuts import render
from .forms import ImageUploadForm
from PIL import Image
import os
from django.conf import settings
from django.core.files import File
import time
from django.core.files.base import ContentFile

def index_view(request):
    return render(request, 'index.html')

def upload_view(request):
    return render(request, 'upload.html')

# views.py
from django.shortcuts import render, redirect
from .forms import MyModelForm
from .models import MyModel
from PIL import Image

def upload_image(request):
    if request.method == 'POST':
        form = MyModelForm(request.POST, request.FILES)
        if form.is_valid():
            instance1_image = form.cleaned_data['instance1']

            # Convert instance1 image to greyscale
            instance1_image = Image.open(instance1_image)
            instance2_image = instance1_image.convert('L')  # 'L' mode is for greyscale

            # Save to the model
            my_model_instance = MyModel()
            my_model_instance.instance1.save(instance1_image.name, instance1_image)
            my_model_instance.instance2.save(instance2_image.name, instance2_image)
            
            context = {
                'original_image_url': instance1_image,
                'grayscale_image_url': instance2_image,
            }

            
            return render(request, 'result.html', context)
    else:
        form = ImageUploadForm()

    return render(request, 'upload.html', {'form': form})

















#Previous Implmenetation

"""def grayscale_image(image_path):
    img = Image.open(image_path).convert('L')
    save_path = os.path.join(settings.MEDIA_ROOT, 'grayscaled')
    os.makedirs(save_path, exist_ok=True)
    grayscale_filename = f"grayscaled_{os.path.basename(image_path)}"
    grayscale_path = os.path.join(save_path, grayscale_filename)

    with open(grayscale_path, 'wb') as f:
        img.save(f, format="JPEG")
    return grayscale_path"""
    
"""def grayscale_image(image_path):
    img = Image.open(image_path).convert('L')
    with BytesIO() as f:
        img.save(f, format="JPEG")
        f.seek(0)
        return f

def upload_image(request):
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_image = form.save(commit=False)
            greyImage = grayscale_image(uploaded_image.image.path)
            
            uploaded_image.grayscale_image_url = f'/media/grayscaled/grayscaled_{os.path.basename(uploaded_image.image.path)}'

            uploaded_image.grayscale_image.save(os.path.basename(uploaded_image.grayscale_image_url), ContentFile(greyImage.getvalue()))

                        
            filename = os.path.basename(uploaded_image.image.path)
            uploaded_image.grayscale_image = f'/media/uploads/{filename}'
            original_image_url = f'/media/uploads/{filename}'

            filename = os.path.basename(uploaded_image.image.path)
            grayscale_image_url = f'/media/grayscaled/grayscaled_{filename}'
            
            uploaded_image.save()

            context = {
                'original_image_url': original_image_url,
                'grayscale_image_url': grayscale_image_url,
            }
            return render(request, 'result.html', context)
    else:
        form = ImageUploadForm()

    return render(request, 'upload.html', {'form': form})"""
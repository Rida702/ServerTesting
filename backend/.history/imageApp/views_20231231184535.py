# views.py
from django.shortcuts import render, redirect
from .forms import ImageUploadForm
from PIL import Image
from io import BytesIO
import base64

def grayscale_image(image_path):
    img = Image.open(image_path).convert('L')
    buffered = BytesIO()
    img.save(buffered, format="JPEG")
    return base64.b64encode(buffered.getvalue()).decode()

def upload_image(request):
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_image = form.save()

            # Process the image and save the grayscale version
            grayscale_data = grayscale_image(uploaded_image.image.path)
            uploaded_image.grayscale_image = f'data:image/jpeg;base64,{grayscale_data}'
            uploaded_image.save()

            return render(request, 'result.html', {'uploaded_image': uploaded_image})
    else:
        form = ImageUploadForm()
    return render(request, 'upload.html', {'form': form})
from django.shortcuts import render

def index_view(request):
    return render(request, 'index.html')
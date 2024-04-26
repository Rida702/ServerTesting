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
    save_path = os.path.join(settings.MEDIA_ROOT, 'grayscaled')
    os.makedirs(save_path, exist_ok=True)
    grayscale_filename = f"grayscaled_{os.path.basename(image_path)}"
    grayscale_path = os.path.join(save_path, grayscale_filename)

    with open(grayscale_path, 'wb') as f:
        img.save(f, format="JPEG")
    return grayscale_path

def upload_image(request):
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_image = form.save(commit=False)  # Don't save the form to the database yet

            # Convert the image to grayscale
            grayscale_path = grayscale_image(uploaded_image.image.path)

            # Save the original and grayscale images in the model
            uploaded_image.image.save(os.path.basename(uploaded_image.image.path), File(open(uploaded_image.image.path, 'rb')))
            uploaded_image.grayscale_image.save(os.path.basename(grayscale_path), File(open(grayscale_path, 'rb')))

            # Save the model to the database
            uploaded_image.save()

            filename = os.path.basename(uploaded_image.image.path)
            grayscale_image_url = f'/media/grayscaled/grayscaled_{filename}'

            context = {
                'uploaded_image': uploaded_image,
                'grayscale_image_url': grayscale_image_url,
            }

            return render(request, 'result.html', context)
    else:
        form = ImageUploadForm()

    return render(request, 'upload.html', {'form': form})
In this modification, form.save(commit=False) is used to create a YourModel instance without saving it to the database. After converting the image to grayscale, both the original and grayscale images are saved in the model, and then the model is saved to the database. This way, both images are uploaded to the model at once.

After making these changes, run python manage.py makemigrations and python manage.py migrate to apply the modifications to the database.

User
from django.db import models

# Create your models with name ImageModel.
class ImageModel(models.Model):
    image = models.ImageField(upload_to='uploads/')
    grayscale_image = models.ImageField(upload_to='grayscaled/', blank=True)

    def save(self, *args, **kwargs):
        if not self.grayscale_image and hasattr(self, 'grayscale_image_url'):
            self.grayscale_image.name = self.grayscale_image_url

        super().save(*args, **kwargs)

from django.db import models
import os

def original_image_path(instance, filename):
    return f'uploads/original_{filename}'

def grayscale_image_path(instance, filename):
    return f'grayscaled/grayscaled_{filename}'

class ImageModel(models.Model):
    image = models.ImageField(upload_to=original_image_path)
    grayscale_image = models.ImageField(upload_to=grayscale_image_path, blank=True)
    grayscale_image_url = models.CharField(max_length=255, blank=True)  # assuming you store the URL in this field

    def save(self, *args, **kwargs):
        if not self.grayscale_image and hasattr(self, 'grayscale_image_url'):
            self.grayscale_image.name = self.grayscale_image_url
            print("This is Grayscale Image path:", self.grayscale_image_url)

        super().save(*args, **kwargs)

        original_image_path = f'media/{self.image.name}'
        print("This is Original Image path:", original_image_path)

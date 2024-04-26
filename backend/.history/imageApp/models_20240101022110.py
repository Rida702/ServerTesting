from django.db import models
import os

class ImageModel(models.Model):
    image = models.ImageField(upload_to='uploads/')
    grayscale_image = models.ImageField(upload_to='grayscaled/', blank=True)
    grayscale_image_url = models.CharField(max_length=255, blank=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        # If grayscale_image_url is not set and image is available, set grayscale_image_url
        if not self.grayscale_image_url and self.image:
            filename = os.path.basename(self.image.path)
            self.grayscale_image_url = f'/media/grayscaled/grayscaled_{filename}'
            self.save(update_fields=['grayscale_image_url'])


    """def save(self, *args, **kwargs):
        if not self.grayscale_image and hasattr(self, 'grayscale_image_url'):
            self.grayscale_image.name = self.grayscale_image_url

        super().save(*args, **kwargs)"""

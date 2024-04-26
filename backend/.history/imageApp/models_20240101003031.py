from django.db import models

# Create your models with name ImageModel.
class ImageModel(models.Model):
    image = models.ImageField(upload_to='uploads/')
    grayscale_image = models.ImageField(upload_to='grayscaled/', blank=True)

    def save(self, *args, **kwargs):
        if not self.grayscale_image and hasattr(self, 'grayscale_image_url'):
            self.grayscale_image.name = self.grayscale_image_url

        super().save(*args, **kwargs)

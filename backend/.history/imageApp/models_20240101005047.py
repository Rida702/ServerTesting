from django.db import models

class ImageModel(models.Model):
    image = models.ImageField(upload_to='uploads/')
    grayscale_image = models.ImageField(upload_to='grayscaled/', blank=True)

    def save(self, *args, **kwargs):
        if not self.grayscale_image and hasattr(self, 'grayscale_image_url'):
            self.grayscale_image.name = self.grayscale_image_url
            print(self.grayscale_image.name)

        super().save(*args, **kwargs)

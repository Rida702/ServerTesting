from django.db import models
import os

class ImageModel(models.Model):
    image = models.ImageField(upload_to='uploads/')
    grayscale_image = models.ImageField(upload_to='grayscaled/', blank=True, null=True)
    #grayscale_image_url = models.CharField(max_length=255, blank=True)

"""    def save(self, *args, **kwargs):
        # If grayscale_image_url is not set and image is available, set grayscale_image_url
        if not self.grayscale_image_url and self.image:
            filename = os.path.basename(self.image.path)
            self.grayscale_image_url = f'/media/grayscaled/grayscaled_{filename}'

        # Call the save method of the parent class
        super().save(*args, **kwargs)
 """
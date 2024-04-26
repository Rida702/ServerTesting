from django.db import models

class ImageModel(models.Model):
    image = models.ImageField(upload_to='uploads/')
    grayscale_image = models.ImageField(upload_to='grayscaled/', blank=True, null=True)
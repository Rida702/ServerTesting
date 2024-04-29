# models.py
from django.db import models

class ImageModel(models.Model):
    watch_image = models.ImageField(upload_to='uploaded_images/')
    wrist_image = models.ImageField(upload_to='uploaded_images/')
    result_image = models.ImageField(upload_to='result_images/', blank=True, null=True)
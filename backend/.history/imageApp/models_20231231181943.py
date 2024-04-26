from django.db import models

# Create your models with name ImageModel.
class ImageModel(models.Model):
    image = models.ImageField(upload_to='/uploads/')

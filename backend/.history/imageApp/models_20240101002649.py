from django.db import models

# Create your models with name ImageModel.
class ImageModel(models.Model):
    image = models.ImageField(upload_to='uploads/')
    grayscale_image = models.ImageField(upload_to='grayscaled/', blank=True)

    def save(self, *args, **kwargs):
        if not self.grayscale_image:
            grayscale_image_path = f'media/greyscaled/{self.image.name.split("/")[-1]}'
            self.grayscale_image.name = grayscale_image_path

        super().save(*args, **kwargs)

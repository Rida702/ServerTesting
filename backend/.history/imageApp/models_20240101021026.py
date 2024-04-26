from django.db import models

class ImageModel(models.Model):
    image = models.ImageField(upload_to='uploads/')
    grayscale_image = models.ImageField(upload_to='grayscaled/', blank=True)

    def save(self, *args, **kwargs):
        # Check if grayscale_image_url attribute is present
        if hasattr(self, 'grayscale_image_url'):
            # Remove the 'media/' prefix from grayscale_image_url
            cleaned_url = self.grayscale_image_url.split('media/', 1)[-1]
            # Assign the cleaned URL to the grayscale_image name
            self.grayscale_image.name = cleaned_url

        super().save(*args, **kwargs)

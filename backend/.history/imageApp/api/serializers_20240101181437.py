from rest_framework import serializers
from ..models import ImageModel

class ImageModel(serializers.ModelSerializer):
    class Meta:
        model = ImageModel
        fields = ['image', 'grayscale_image']
        
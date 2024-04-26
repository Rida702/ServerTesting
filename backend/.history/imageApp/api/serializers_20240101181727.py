from rest_framework import serializers
from ..models import ImageModel

class ImageModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageModel
        fields = ['id', image', 'grayscale_image']
        
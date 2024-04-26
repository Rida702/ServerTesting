from rest_framework import serializers
from .models import ImageModel

class ImageModel(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ['id','name','description','qr_code','date']
        
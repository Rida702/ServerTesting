from rest_framework import serializers
from ..models import Event

class ImageModel(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ['id','name','description','qr_code','date']
        
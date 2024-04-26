from rest_framework import viewsets
from ..models import ImageModel
from .serializers import ImageModelSerializer

class ImageViewSet(viewsets.ModelViewSet):
    queryset = ImageModel.objects.all()
    serializer_class = ImageModelSerializer
from rest_framework import viewsets
from ..models import ImageModel
from .serializers import ImageModelSerializer

class EventsViewSet(viewsets.ModelViewSet):
    queryset = ImageModel.objects.all()
    serializer_class = ImageModelSerializer
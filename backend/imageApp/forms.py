# forms.py
from django import forms
from .models import ImageModel

class ImageUploadForm(forms.ModelForm):
    class Meta:
        model = ImageModel
        fields = ['watch_image', 'wrist_image']
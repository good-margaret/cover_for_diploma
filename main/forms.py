from django import forms
from .models import ImageRestoration

class ImageUploadForm(forms.ModelForm):
    class Meta:
        model = ImageRestoration
        fields = ['original_image']
from django import forms
from .models import Design

class DesignUploadForm(forms.ModelForm):
    class Meta:
        model = Design
        fields = ['title', 'description', 'design_file']
# forms.py
from django import forms
from .models import Resource

class ResourceForm(forms.ModelForm):
    agency_name = forms.CharField(max_length=255, required=True)

    class Meta:
        model = Resource
        fields = ['name', 'quantity', 'agency_name'] 

class ResourceUploadForm(forms.Form):
    file = forms.FileField()
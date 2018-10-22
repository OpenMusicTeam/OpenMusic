from django import forms
from django.forms import ModelForm
from .models import FileModel

class UploadFileForm(ModelForm):
   
    class Meta:
        model = FileModel
        fields = ['title', 'data',]

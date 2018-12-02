from django import forms
from django.forms import ModelForm
from .models import FileModel

class UploadFileForm(ModelForm):
   
    class Meta:
        model = FileModel
        fields = ['title', 'data',]
        widgets = {
            'title': forms.TextInput(attrs=
            {
                'id': 'customFileTitle',
                'class': 'form-control',
                'placeholder': 'Enter a file title...',
            }),
            'data': forms.FileInput(attrs=
            {
                'id': 'customFile',
                'class': 'custom-file-input',
            }),
        }
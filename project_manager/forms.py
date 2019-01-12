from django import forms
from django.forms.models import ModelForm
from file_upload.models import FileModel
from .models import Project

class ProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = ['name', 'desc',]
        widgets = {
            'name': forms.TextInput(attrs=
            {
                'class': 'form-control',
                'placeholder': 'Enter a project name...',
            }),
            'desc': forms.TextInput(attrs=
            {
                'class': 'form-control',
                'placeholder': 'Enter a project description...',
            }),
        }

class ProjectAddContributorForm(ModelForm):
    class Meta:
        model = Project
        fields = ['contributors',]
        widgets = {
            'contributors': forms.SelectMultiple(attrs=
            {
                'id': 'customFile',
                'class': 'form-control formSelect',
            }),
        }

class ProjectPublishForm(ModelForm):

    class Meta:
        model = FileModel
        fields = ['description', 'genre', 'project_publish_image_url',]
        
        
        
       
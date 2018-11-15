from django import forms
from django.forms.models import ModelForm

from .models import Project

class ProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = ['name', 'desc',]

class ProjectAddContributorForm(ModelForm):
    class Meta:
        model = Project
        fields = ['contributors',]
    
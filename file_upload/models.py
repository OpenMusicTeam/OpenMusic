from django.db import models
from .upload_validator import FileValidator
from django.contrib.auth.models import User
from django.conf import settings
from django.contrib.auth import get_user_model
from project_manager.models import Project
import os

class FileModel(models.Model):
    #user = models.ForeignKey(User, on_delete=models.CASCADE)
    #user = get_user_model()
    #user = instance.username

    title = models.CharField(max_length=50)
    data = models.FileField(validators= [FileValidator(max_size=24*1024*1024, allowed_extensions=('mp3', 'jpg'))])
    userProfile = models.ForeignKey(User, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, blank=True, null=True)
    

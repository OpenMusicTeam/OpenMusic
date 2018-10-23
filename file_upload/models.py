from django.db import models
from .upload_validator import FileValidator
from django.contrib.auth.models import User
 
class FileModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    data = models.FileField(upload_to='user_projects/'+user,validators= [FileValidator(max_size=24*1024*1024, allowed_extensions=('mp3', 'jpg'))])
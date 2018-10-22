from django.db import models
from .upload_validator import FileValidator
 
class FileModel(models.Model):
    title = models.CharField(max_length=50)
    data = models.FileField(upload_to='accounts/static/accounts/audio/',validators= [FileValidator(max_size=24*1024*1024, allowed_extensions=('mp3', 'jpg'))])

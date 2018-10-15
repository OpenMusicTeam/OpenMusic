from django.db import models
 
class FileModel(models.Model):
    title = models.CharField(max_length=50)
    data = models.FileField(upload_to='uploads/')

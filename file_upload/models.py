from django.db import models
from .upload_validator import FileValidator
from django.contrib.auth.models import User
from django.conf import settings
from django.contrib.auth import get_user_model
import os

def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    #result = 'user_projects/%s/%s' % (instance.user.id, filename)
    #result = 'user_{0}/{1}'.format(instance.user.id, filename)
    #print(result)
    #return result
    print(instance.id)
    return os.path.join('user_projects', str(instance.slug), filename)

class FileModel(models.Model):
    #user = models.ForeignKey(User, on_delete=models.CASCADE)
    #user = get_user_model()
    #user = instance.username

    title = models.CharField(max_length=50)
    data = models.FileField(upload_to=user_directory_path,validators= [FileValidator(max_size=24*1024*1024, allowed_extensions=('mp3', 'jpg'))])

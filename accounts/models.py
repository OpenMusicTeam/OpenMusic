from django.contrib.auth.models import User
from django.db import models


class UserProfile(models.Model):
    user = models.OneToOneField(User , on_delete=models.CASCADE)
    age = models.IntegerField(default=0, blank=True)
    desc = models.CharField(max_length=140,blank=True)
    avatar = models.ImageField(upload_to='avatars/',default='avatars/default.png', blank=True)

    def __str__(self):
    	return str(self.user)
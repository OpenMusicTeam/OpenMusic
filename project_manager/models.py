from django.db import models
from django.contrib.auth.models import User
from accounts.models import UserProfile

class Project(models.Model):
    name = models.CharField(max_length=50)
    desc = models.CharField(max_length=140,blank=True)
    userProfile = models.ForeignKey(User, on_delete=models.CASCADE)
    contributors = models.ManyToManyField(UserProfile)

    def __str__(self):
    	return (self.name)
from django.db import models
from .upload_validator import FileValidator
from django.contrib.auth.models import User
from django.conf import settings
from accounts.models import UserProfile
from django.contrib.auth import get_user_model
from project_manager.models import Project
import os
from django.utils import timezone

class FileModel(models.Model):
    #user = models.ForeignKey(User, on_delete=models.CASCADE)
    #user = get_user_model()
    #user = instance.username

    title = models.CharField(max_length=50)
    data = models.FileField(validators= [FileValidator(max_size=24*1024*1024, allowed_extensions=('mp3', 'wav'))])
    userProfile = models.ForeignKey(User, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, blank=True, null=True)
    project_publish_resource = models.ForeignKey(Project, on_delete=models.CASCADE, related_name = 'project_publish_resource', null=True)
    genre=models.CharField(max_length=50, null=True)
    project_publish_image_url=models.CharField(max_length=500, null=True, default = "https://res.cloudinary.com/easymedicine/image/upload/v1547204544/DefaultSongImage.png")
    likes=models.ManyToManyField(User, related_name="likes")
    description= models.CharField(max_length=500, null=True)

    def __str__(self):
    	return str(self.title) 

    def total_likes(self):
        return self.likes.count()

    def get_likes(self):
        return self.likes

class CommentModel(models.Model):
    comments=models.ManyToManyField(FileModel)
    author = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)

    def total_comments(self):
        return self.comments.count()

from datetime import datetime

from django.conf import settings
from django.db import models


class Post(models.Model):
    content = models.TextField()
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='post')
    likes = models.IntegerField(default=0)
    created_at = models.DateTimeField(default=datetime.now, blank=True)


class UserPostLike(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='post_like_rel')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='user_like_rel')
    value = models.IntegerField()
    updated_at = models.DateTimeField(auto_now=True, blank=True)

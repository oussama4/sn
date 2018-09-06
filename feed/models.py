from django.db import models
from django.conf import settings
from django.contrib.contenttypes.models import ContentType

class Post(models.Model):
    """
    a news feed post
    """

    text = models.TextField()
    image = models.ImageField(upload_to='posts/%Y/%m/%d')

class Action(models.Model):
    """
    represents a news feed action
    """

    actor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, 
        related_name='actions', db_index=True)
    verb = models.CharField(max_length=50)
    target = models.ForeignKey(Post, on_delete=models.CASCADE, null=True, blank=True)
    target_actor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-created',)

class Comment(models.Model):
    """
    a model for news feed comments
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, db_index=True)
    action = models.ForeignKey(Action, on_delete=models.CASCADE,
        related_name='comments', db_index=True)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('created',)

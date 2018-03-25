from django.db import models
from django.conf import settings

class Room(models.Model):
    """
    a chat room model
    """

    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        related_name='created_rooms')
    members = models.ManyToManyField(settings.AUTH_USER_MODEL, 
        related_name='rooms')
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True, null=True)
    public = models.BooleanField()
    created = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name

class Message(models.Model):
    """
    chat message
    """

    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        related_name='chat_messages')
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.body[:10] + ' ...'

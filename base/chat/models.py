from django.db import models

class Message(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.CharField(max_length=100, default='')
    text_message = models.TextField()
    date = models.DateTimeField(null=True, default=None)
    room = models.CharField(max_length=100, default='room')

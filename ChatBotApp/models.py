from django.db import models

class Conversation(models.Model):
    user_id = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

class Message(models.Model):
    conversation = models.ForeignKey(Conversation, related_name='messages', on_delete=models.CASCADE)
    sender = models.CharField(max_length=10)  # 'user' hoặc 'bot'
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
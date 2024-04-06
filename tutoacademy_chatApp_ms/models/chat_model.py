from django.db import models
from djongo import models as mdls
from django.utils import timezone


#Model message structure to use in Chat model
class Message(models.Model):
    messageId = models.IntegerField(primary_key=True)
    sender = models.CharField(max_length=100)
    body = models.TextField()
    sendTime = models.DateTimeField(timezone.now)
        


#Model for creation a Chat beetween a pair of users ()
class Chat(models.Model):
    chatId= models.AutoField(primary_key=True)
    sender= models.CharField(max_length=100)
    receiver= models.CharField(max_length=100)
    messages = mdls.ArrayField(
        model_container=Message
    )
    state = models.BooleanField(default=True)
    createTime = models.DateTimeField(auto_now_add=True)
    
    
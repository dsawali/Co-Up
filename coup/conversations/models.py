from django.db import models
from django.conf import settings
from ..core.models import TimeStampedModel

class Group(TimeStampedModel):
    """
    Groups may be declared mutable or immutable. A mutable group may not have
    new members added, but all other fields can be modified.
    """
    name = models.CharField(null=False, blank=False, max_length=64)
    subject = models.CharField(null=False, blank=False, max_length=128)
    description = models.TextField(null=False, blank=False)
    locked = models.BooleanField(default=False)
    users = models.ManyToManyField(settings.AUTH_USER_MODEL)
    
    def __str__(self):
        return self.name
    

class Conversation(TimeStampedModel):
    """
    Conversations represent a conversation regarding a single subject. Each
    conversation is associated with a single group.
    """
    group = models.ForeignKey(Group, on_delete=models.CASCADE, null=True)
    subject = models.CharField(null=False, blank=True, max_length=64)
    def __str__(self):
        return self.subject
    
    
class Message(TimeStampedModel):
    """
    Messages represent a single message in a conversation. Each message is
    associated with one user.
    """
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    text = models.TextField(null=False, blank=False)
    def __str__(self):
        return self.text

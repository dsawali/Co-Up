from django.contrib import admin
from .models import Group, Message, Conversation

admin.site.register(Group)
admin.site.register(Message)
admin.site.register(Conversation)


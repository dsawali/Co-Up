from django.contrib import admin

from coup.positions.models import Comment, Position
# Register your models here.
from django.contrib import admin
from .models import Position, Comment
"""
enable admin control to edit Position and Comment Models
as necessary.
"""

class PositionAdmin(admin.ModelAdmin):
    """
    Custom model admin for position.
    """ 
    model = Position
    list_display = ['username']
    prepopulated_fields = {
        'slug' : ('title', 'company'),
    }   

    def username(self,\
                 obj):
        return obj.user.username

admin.site.register(Position, PositionAdmin)
admin.site.register(Comment)

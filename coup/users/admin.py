# from django.contrib import admin
#
# # Register your models here.


# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from coup.users.models import User
from .models import User

from .models import User


class UserAdmin(admin.ModelAdmin):
    """
    Custom model admin for user.
    """
    # prepopulate slug to be username
    prepopulated_fields = {
        'slug' : ('username',)
    }

admin.site.register(User, UserAdmin)

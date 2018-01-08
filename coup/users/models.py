from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager
from django.core.urlresolvers import reverse

from config import settings
import os
import json

#------------------------------------------------- helper functions
def getChoices():
    """
    coverts dictionary from json to tuples
    used by program field in ProfileForm
    """
    dirr = os.path.join(os.path.dirname(settings.settings.BASE_DIR), 'config')
    #default_t = ('Not specified', 'Not specified')
    with open(os.path.join(dirr, "SFU_program_data.json")) as f:
        json_data = json.load(f)
        choice_list = []
        for faculty in json_data:
            programs = json_data[faculty]
            for program in programs:
                choice_list.append((program, program))
    return tuple (choice_list)

def get_user_dir_path(instance,\
                      filename):
    """
    profile picture saved at 
    MEDIA_ROOT/profile_pictures/username/filename
    """
    return 'profile_pictures/{0}/{1}'.format(\
        instance.slug,\
        filename)

#---------------------------------------------------- models
class UserManager(UserManager):
    """
    Custom model manager extending
    over django's default model manager.
    """
    DEFAULT_FACULTY = 'Not specified'
    DEFAULT_PROGRAM = 'Not specified'

    def query_on_params(self,\
                        **kwargs):
        """
        Method called by search view
        to filter users on:
            - username
            - firstname + lastname
            - lastname
            - faculty
            - program
        """
        if self.check_empty_query(**kwargs):
            return []
        
        elif 'username' in kwargs and len(kwargs) == 1:
            name = kwargs['username'][0]
            return self.query_on_name(\
                name,\
                self.all()) 

        username_s = kwargs['username'][0]
        fullname_s = kwargs['fullname'][0]
        faculty_s = kwargs['faculty'][0]
        program_s = kwargs['program'][0]
        query_set_l = self.all()
        if username_s != '':
            query_set_l = query_set_l.filter(\
                username__icontains = username_s)
        if fullname_s != '':
            query_set_l = self.query_on_name(\
                fullname_s,\
                query_set_l)
        if faculty_s != '':
            query_set_l = query_set_l.filter(\
                faculty__exact = faculty_s)
        if program_s != '':
            query_set_l = query_set_l.filter(\
                program__exact = program_s)
        return query_set_l

    def check_empty_query(self,\
                          **kwargs):
        """
        Checks if user has not specified
        any fields on search form.
        """
        for value in kwargs.values():
            if value[0] != '' and \
                value != self.DEFAULT_FACULTY and \
                value != self.DEFAULT_PROGRAM:
                return False
        return True

    def query_on_name(self,\
                      name_s,\
                      query_set_l):
        """
        Parses string to match for 
        username/firstname/lastname.
        """
        if ' ' in name_s:
            name_l = name_s.split(' ')
            query_set_l = query_set_l.filter(\
                first_name__icontains = name_l[0],\
                last_name__icontains = name_l[1])
        else:
            query_set_l = query_set_l.filter(\
                models.Q(first_name__icontains = name_s) |\
                models.Q(last_name__icontains = name_s))
        return query_set_l


class User(AbstractUser):
    """
    Custom User model extending on AbstractUser.
    NOTE: REFER TO 'django.conf.settings.AUTH_USER_MODEL'
          WHEN CREATING RELATIONSHIPS TO THIS MODEL
    TODO: PROGRAM CHOICES FOR EACH FACULTY.
    """
    # add custom manager
    objects = UserManager()

    FACULTY_CHOICES = (
        ('Sciences', 'Sciences'),
        ('Applied Sciences', 'Applied Sciences'),
        ('Business', 'Business'),
        ('Education', 'Education'),
        ('Environment', 'Environment'),
        ('Communication, Art and Technology', 'Communication, Art and Technology'),
        ('Health Sciences', 'Health Sciences'),
        ('Arts and Sco', 'Arts and Sco')
    )

    PROGRAM_CHOICES = getChoices()

    # academic information
    faculty = models.CharField(max_length=30, \
        choices = FACULTY_CHOICES,\
        blank = True)
    program = models.CharField(max_length=30,\
        choices = PROGRAM_CHOICES,\
        blank = True)

    # optional user description
    bio = models.TextField(null=True, \
        blank = True)

    # profile picture
    picture = models.ImageField(\
        upload_to = get_user_dir_path,\
        default = 'profile_pictures/default.png')

    # slug for meaningful profile url
    slug = models.SlugField()

    def __str__(self):
        return "%s" % (self.username)

    def generate_slug(self):
        """
        Sets slug for user profile URL 
        as user's username.
        """
        self.slug = self.username

    def get_absolute_url(self):
        """
        constructs a url for the user model
        """
        return reverse('users:view_profile',\
            kwargs={'slug': self.slug})



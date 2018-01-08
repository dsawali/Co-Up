from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin, AccessMixin
from django.contrib import admin, messages
from django.contrib.auth import views as auth_views
from django.views.generic import DetailView, UpdateView
from django.urls import reverse
from django.http import Http404

from .models import User
from .forms import ProfileForm
from coup.user_auth.views import ErrorView

import urllib.request
import xml.etree.ElementTree as ET


class UserActionMixin(object):
    """
    Mixin to be inherited by UserProfileView
    and UserProfileEditView for update confirmation.
    """
    fields = ['picture',\
        'first_name',\
        'last_name',\
        'faculty',\
        'program',\
        'bio']

    @property
    def success_msg(self):
        return NotImplemeted

    def form_valid(self,\
                   form):
        """
        Displays success message on valid form.
        """
        messages.info(self.request,\
            self.success_msg)
        return super(UserActionMixin, self).\
            form_valid(form)


class UserDetailView(LoginRequiredMixin,\
                     UserActionMixin,\
                     DetailView):
    """
    View to render logged in user's profile details.
    """
    login_url = '/login/'
    model = User
    template_name = 'users/view_profile.html'


class UserUpdateView(LoginRequiredMixin,\
                     UserActionMixin,\
                     UpdateView):
    """
    View to render profile edit form 
    for a logged in user.
    """
    # authentication
    login_url = '/login/'

    # view specific parameters
    model = User
    template_name = 'users/update_profile.html'
    success_msg = 'Profile updated'

    def dispatch(self,\
                 request,\
                 *args,\
                 **kwargs):
        if self.request.user != self.get_object():
            return HttpResponseRedirect('/user_auth/error/')
        return super(UserUpdateView, self).dispatch(\
            request,\
            *args,\
            **kwargs)

    def get_success_url(self):
        return reverse('users:view_profile', \
            kwargs = { 'slug' : self.object.slug }
        )



# @login_required
# def account_redirect(request):
#     # url = '/users/'+str(request.user.username)+'/profile'
#     return redirect('/')

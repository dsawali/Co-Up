from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.views.generic.base import TemplateView, RedirectView
from django.contrib import messages


from .forms import SignUpForm
from ..users.models import User
from .models import Contact
from coup.common.decorators import ajax_required
from coup.actions.models import Action
from coup.actions.utils import create_action

# Create your views here.

def signup(request):
    """
    A function that renders registeration form to add new user.
    """
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            # Create a new user object but do not save it yet
            new_user = form.save(commit=False)
            # set slug for new user
            new_user.generate_slug()
            # Set the chosen password
            # new_user.set_password(form.cleaned_data['password'])
            # new_user
            # Save the User object
            new_user.save()
            # Create the user profile
            # profile = User.objects.create(user=new_user)
            return render(request,
                          'user_auth/signup_done.html',
                          {'new_user': new_user})
    else:
        form = SignUpForm()
    return render(request, 'user_auth/signup.html', {'form': form})


    #return render(request, 'user_auth/signup.html', {'form': form})

@login_required
def user_list_followers(request):
    """
    Get the list of active users - who are currently logged in.
    We can add pagination here to display paginated list.
    """
    users = User.objects.filter(is_active=True)
    return render(request, 'user_auth/user/followers.html', {'section': 'people',
                                                      'users': users})

@login_required
def user_list_following(request):
    """
    Get the list of active users - who are currently logged in.
    We can add pagination here to display paginated list.
    """
    users = User.objects.filter(is_active=True)
    return render(request, 'user_auth/user/following.html', {'section': 'people',
                                                      'users': users})

@login_required
def user_detail(request, username):
    user = get_object_or_404(User, username=username, is_active=True)
    return render(request, 'user_auth/user/detail.html', {'section': 'people',
                                                        'user': user})

@ajax_required
@require_POST
@login_required
def user_follow(request):
    user_id = request.POST.get('id')
    action = request.POST.get('action')
    if user_id and action:
        try:
            user = User.objects.get(id=user_id)
            if action == 'follow':
                Contact.objects.get_or_create(user_from=request.user,
                                              user_to=user)
                create_action(request.user, 'is following', user)
            else:
                Contact.objects.filter(user_from=request.user,
                                       user_to=user).delete()
            return JsonResponse({'status':'ok'})
        except User.DoesNotExist:
            return JsonResponse({'status':'ko'})
    return JsonResponse({'status':'ko'})


class LoginRedirectView(RedirectView):
    """
    Redirects user to /user_auth/login/ when
    visting /login/, /log-in/, etc.
    """
    pattern_name = 'login'


class LogoutRedirectView(RedirectView):
    """
    Redirects user to /user_auth/logout/ when
    visiting /logout/log-out, etc.
    """
    pattern_name = 'logout'


class ErrorView(TemplateView):
    """
    User will get redirected to this view
    upon making an un-authorized request.
    """
    template_name = 'user_auth/error.html'

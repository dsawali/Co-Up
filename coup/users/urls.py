from django.conf.urls import url
from django.contrib.auth import views as auth_views

from . import views
from coup.user_auth.views import LoginRedirectView, LogoutRedirectView

app_name = 'users'
urlpatterns = [
    url(
        r'^(?P<slug>[a-zA-Z0-9]+)/profile/$',\
        views.UserDetailView.as_view(),\
         name="view_profile"
    ),
    url(
        r'^(?P<slug>[a-zA-Z0-9]+)/profile/edit/$',\
        views.UserUpdateView.as_view(),\
         name="update_profile"
    ),
    url(
        r'^login/$',\
        LoginRedirectView.as_view(),\
        name='login-redirect'
    ),
    url(
        r'^log-in/$',\
        LoginRedirectView.as_view(),\
        name='login-redirect'
    ),
    url(
        r'^logout/$',\
        LogoutRedirectView.as_view(),\
        name='logout-redirect'
    ),
    url(
        r'^log-out/$',\
        LogoutRedirectView.as_view(),\
        name='logout-redirect'
    )    
    # url(r'^account_redirect/$', views.account_redirect, name='account-redirect')

]

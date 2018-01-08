from django.conf.urls import url, include
from django.contrib.auth import views as auth_views
from . import views


urlpatterns = [
    url(r'^error/$', views.ErrorView.as_view(), name='error'),

    url(r'^signup/$', views.signup, name='signup'),

    # url(r'^edit/$', views.edit, name='edit'),
    # login / logout urls
    url(r'^login/$', auth_views.login, name='login'),

    # url(r'^login/$', views.user_login, name='user_login'),
    url(r'^logout/$', auth_views.logout, name='logout'),
    url(r'^logout-then-login/$', auth_views.logout_then_login, name='logout_then_login'),

    # change password urls
    url(r'^password-change/$', auth_views.password_change, name='password_change'),
    url(r'^password-change/done/$', auth_views.password_change_done, name='password_change_done'),

    # restore password urls
    url(r'^password-reset/$', auth_views.password_reset, name='password_reset'),
    url(r'^password-reset/done/$', auth_views.password_reset_done, name='password_reset_done'),
    url(r'^password-reset/confirm/(?P<uidb64>[-\w]+)/(?P<token>[-\w]+)/$', auth_views.password_reset_confirm, name='password_reset_confirm'),
    url(r'^password-reset/complete/$', auth_views.password_reset_complete, name='password_reset_complete'),

    # user follower system urls
    url(r'^users/followers/$', views.user_list_followers, name='user_list_followers'),
    url(r'^users/following/$', views.user_list_following, name='user_list_following'),
    url(r'^users/follow/$', views.user_follow, name='user_follow'),
    url(r'^users/(?P<username>[-\w]+)/$', views.user_detail, name='user_detail'),

    # python-social-auth
    url('social-auth/', include('social.apps.django_app.urls', namespace='social')),
]

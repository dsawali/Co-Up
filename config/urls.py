"""coup URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.conf.urls.static import static

from .settings import settings
from coup.user_auth.views import LoginRedirectView, LogoutRedirectView


urlpatterns = [
    url(r'^conversations/', include('coup.conversations.urls', namespace='conversations')),
    url(r'^admin/', admin.site.urls),
    url(r'^', include('coup.dashboard.urls', namespace='dashboard')),
    url(r'^search/', include('coup.search.urls', namespace='search')),
    url(r'^positions/', include('coup.positions.urls', namespace='positions')),
    url(r'^users/', include ('coup.users.urls')),

    url(r'^user_auth/', include('coup.user_auth.urls')),
    # python-social-auth
    url('social-auth/', include('social.apps.django_app.urls', namespace='social')),

    # login redirects
    url(r'^login/$', LoginRedirectView.as_view(), name='login-redirect'),
    url(r'^log-in/$', LoginRedirectView.as_view(), name='login-redirect'),

    # logout redirects
    url(r'^logout/$', LogoutRedirectView.as_view(), name='logout-redirect'),
    url(r'^log-out/$', LogoutRedirectView.as_view(), name='logout-redirect'),

] +\
static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

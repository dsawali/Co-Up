from django.conf.urls import url
from django.contrib import admin

from . import views
from ..api import views as api

urlpatterns = [
    url(
        regex = r'^$',\
        view = views.SearchView.as_view(),\
        name = 'searchView'
    ),
    url(
        regex = r'^api/get_titles',\
        view = api.get_titles,\
        name = 'get_titles'
    ),
    url(
        regex = r'^api/get_companies',\
        view = api.get_companies,\
        name = 'get_companies'
    ),
    url(
        regex = r'^api/get_usernames',\
        view = api.get_usernames,\
        name = 'get_usernames'
    ),
    url(
        regex = r'^api/get_fullnames',\
        view = api.get_fullnames,\
        name = 'get_fullnames'
    ),
    url(r'^admin/', admin.site.urls),
]

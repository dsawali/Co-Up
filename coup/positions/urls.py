from django.conf.urls import url, include
from . import views


app_name = 'positions'
urlpatterns = [
    url(r'^overview/$', views.PositionListView.as_view(), name='index'),
    url(r'^add/$', views.add_position, name='add-position'),
    url(r'^(?P<pk>\d+)-(?P<slug>[-\w\d]+)/', include([
        url(r'^detail/$', views.PositionDetailView.as_view(), name='position-detail'),
        url(r'^edit/$', views.edit_position, name='edit-position'),
        url(r'^delete/$', views.delete_position, name='delete-position'),
    ])),
]

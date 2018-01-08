"""conversations URL Configuration

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
from django.conf.urls import url
from .views import GroupList, GroupDetail, GroupCreate, GroupUpdate,\
    GroupDelete, ConversationList, ConversationDetail, ConversationCreate,\
    ConversationUpdate, ConversationDelete, MessageCreate, ConversationInitial,\
    GroupListAjax, ConversationListAjax, MessageListAjax, MessageCreateAjax

urlpatterns = [
    url(r'^groups/$', GroupList.as_view(), name='group-list'),
    url(r'^groups/create/$', GroupCreate.as_view(), name='group-create'),
    url(r'^groups/(?P<pk>\d+)/$', GroupDetail.as_view(), name='group-detail'),
    url(r'^groups/(?P<pk>\d+)/update/$', GroupUpdate.as_view(), name='group-update'),
    url(r'^groups/(?P<pk>\d+)/delete/$', GroupDelete.as_view(), name='group-delete'),
    url(r'^$', ConversationInitial.as_view(), name='conversation-initial'),
    url(r'^list/$', ConversationList.as_view(), name='conversation-list'),
    url(r'^create/$', ConversationCreate.as_view(), name='conversation-create'),
    url(r'^(?P<pk>\d+)/$', ConversationDetail.as_view(), name='conversation-detail'),
    url(r'^(?P<pk>\d+)/update/$', ConversationUpdate.as_view(), name='conversation-update'),
    url(r'^(?P<pk>\d+)/delete/$', ConversationDelete.as_view(), name='conversation-delete'),
    url(r'^(?P<pk>\d+)/create/$', MessageCreate.as_view(), name='message-create'),
    url(r'^group-list-ajax/$', GroupListAjax, name='group-list-ajax'),
    url(r'^conversation-list-ajax/$', ConversationListAjax, name='conversation-list-ajax'),
    url(r'^message-list-ajax/$', MessageListAjax, name='message-list-ajax'),
    url(r'^message-create-ajax/$', MessageCreateAjax, name='message-create-ajax'),
]

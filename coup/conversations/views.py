from django.shortcuts import render, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.base import TemplateView
from .models import Group, Conversation, Message
from ..users.models import User # This needs to be abstracted away
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods, require_GET, require_POST
from django.http import HttpResponse, HttpResponseBadRequest
from functools import wraps
from django.forms import modelform_factory
import json



# Could use something like this to restrict user
def group_contains_user(group, user):
    if group.users_set.filter(pk = user.pk):
        return True
    else:
        return False
        
# Could use something like this to restrict user
def conversation_contains_user(conversation, user):
    if conversation.group.users_set.filter(pk = user.pk):
        return True
    else:
        return False
        
# This needs fixing
def require_AJAX(view):
    @wraps(view)
    def wrap(request, *args, **kwargs):
        if request.is_ajax():
            return view(request, *args, **kwargs)
        else:
            return HttpResponseBadRequest()
        
'''
AJAX views. These views are to be called to update the content rendered in the initial view
Should we do something about require https?
'''
@login_required
#@require_AJAX
@require_POST
def GroupListAjax(request):
    template_name = 'conversations/group_list_ajax.html'
    begin = request.POST.get('begin', 0)
    count = request.POST.get('count', 10)
    try:
        begin = int(begin)
        count = int(count)
    except:
        return HttpResponseBadRequest()
        
    if begin < 0 or count < 0:
        return HttpResponseBadRequest()
    
    # Get the users groups
    context = {}
    context['groups_list'] = Group.objects.filter(users__pk = request.user.pk).order_by('-modified')[begin:begin+count]
    content_type = 'text/html'
    print (render(request, template_name, context, content_type))
    return render(request, template_name, context, content_type)

@login_required
#@require_AJAX
@require_POST
def ConversationListAjax(request):
    template_name = 'conversations/conversation_list_ajax.html'
    group = request.POST.get('group', None)
    begin = request.POST.get('begin', 0)
    count = request.POST.get('count', 10)
    if group is None:
        return HttpResponseBadRequest()
    try:
        group = int(group)
        begin = int(begin)
        count = int(count)
    except:
        return HttpResponseBadRequest()
    if begin < 0 or count < 0:
        return HttpResponseBadRequest()
        
    # Check that the group exists and the user is a member
    get_object_or_404(Group, pk = group, users__pk = request.user.pk)
    
    context = {}
    context['conversations_list'] = Conversation.objects.filter(group__pk = group).order_by('-modified')[begin:begin+count]
    content_type = 'text/html'
    print (context)
    return render(request, template_name, context, content_type)

@login_required
#@require_AJAX
@require_POST
def MessageListAjax(request):
    template_name = 'conversations/message_list_ajax.html'
    conversation = request.POST.get('conversation', None)
    begin = request.POST.get('begin', 0) # default to origin
    count = request.POST.get('count', 10) # default to 10
    if conversation is None:
        return HttpResponseBadRequest()
    try:
        conversation = int(conversation)
        begin = int(begin)
        count = int(count)
    except:
        return HttpResponseBadRequest()
    if begin < 0 or count < 0:
        return HttpResponseBadRequest()
        
    # Check that the conversation exists and the user is a member of the group
    get_object_or_404(Conversation, pk = conversation, group__users__pk = request.user.pk)
    
    context = {}
    context['messages_list'] = reversed(Message.objects.filter(\
                conversation__pk = conversation).order_by('-created')[begin:begin+count])
    content_type = 'text/html'
    return render(request, template_name, context, content_type)
    
@login_required
#@require_AJAX
@require_POST
def MessageCreateAjax(request):
    template_name = 'conversations/message_create_ajax.html'
    conversation = request.POST.get('conversation', None)
    if conversation is None:
        return HttpResponseBadRequest()
    message = str(request.POST.get('message', '')) # Should we allow empty messages?
    if message == '': # We are disallowing empty messages and missing arguments
        return HttpResponseBadRequest()
    
    # Check that the conversation exists and the user is a member of the group
    get_object_or_404(Conversation, pk = conversation, group__users__pk = request.user.pk)
    
    # Create the message
    message_data = {}
    message_data['user'] = request.user.pk
    message_data['conversation'] = conversation
    message_data['text'] = message
    message_modelform = modelform_factory(Message, fields = '__all__')
    message_form = message_modelform(message_data)
    
    if message_form.is_valid():
        message_form.save()
        return HttpResponse()
    else:
        return HttpResponseBadRequest()

        
'''
The initial view of conversations. Context contains the all the users groups, the last 10 conversations in the 
latest group, and the last 10 messages in the latest conversation.
'''     
class ConversationInitial(LoginRequiredMixin, TemplateView):
    template_name = "conversations/conversations.html"
    def get_context_data(self, **kwargs):
        context = super(ConversationInitial, self).get_context_data(**kwargs)     
        # Groups: All groups that user is a member of
        context['groups_list'] = Group.objects.filter(users__pk = self.request.user.pk).order_by('-modified')[:5]
        # Conversations: All conversations in the first group
        if context['groups_list']:
            context['conversations_list'] = Conversation.objects.filter(group__pk = context['groups_list'][0].pk).order_by('-modified')[:5]
        else:
            context['conversations_list'] = None
        # Messages: Last 10 messages in the above conversation
        if context['conversations_list']:
            context['messages_list'] = reversed(Message.objects.filter(\
                conversation__pk = context['conversations_list'][0].pk).order_by('-created')[:100])
        else:
            context['messages_list'] = None
        return context

class GroupList(LoginRequiredMixin, ListView):
    def get_queryset(self):
        return Group.objects.filter(users__pk = self.request.user.pk)

class GroupDetail(LoginRequiredMixin, DetailView):
    model = Group
    def get_context_data(self, **kwargs):
        # Check that the group exists and the user is a member
        get_object_or_404(Group, pk = self.object.pk, users__pk = self.request.user.pk)
        # Call the base implementation first to get a context
        context = super(GroupDetail, self).get_context_data(**kwargs)
        return context

class GroupCreate(LoginRequiredMixin, CreateView):
    model = Group
    fields = '__all__'
    def get_success_url(self):
        return reverse_lazy('conversations:group-list')

class GroupUpdate(LoginRequiredMixin, UpdateView):
    model = Group
    def get_form(self):
        if Group.objects.get(pk = self.object.pk).locked:
            self.fields = ['name', 'subject', 'description']
        else:
            self.fields = ['name', 'subject', 'description', 'users']
        return super(GroupUpdate, self).get_form()
    
    def get_success_url(self):
        return reverse_lazy('conversations:group-detail', kwargs = {'pk' : self.object.pk})

class GroupDelete(LoginRequiredMixin, DeleteView):
    template_name = 'conversations/delete_confirm.html'
    model = Group
    success_url = reverse_lazy('conversations:group-list')
    def get_context_data(self, **kwargs):
        # Check that the group exists and the user is a member
        get_object_or_404(Group, pk = self.object.pk, users__pk = self.request.user.pk)
        # Call the base implementation first to get a context
        context = super(GroupDelete, self).get_context_data(**kwargs)
        return context
    
class ConversationList(LoginRequiredMixin, ListView):
    def get_queryset(self):
        return Conversation.objects.filter(group__users__pk = self.request.user.pk)
    
class ConversationDetail(LoginRequiredMixin, DetailView):
    model = Conversation
    def get_context_data(self, **kwargs):
        # Check that the conversation exists and the user is a member of the group
        get_object_or_404(Conversation, pk = self.object.pk, group__users__pk = self.request.user.pk)
        # Call the base implementation first to get a context
        context = super(ConversationDetail, self).get_context_data(**kwargs)
        # Add in all messages in this conversation
        context['conversation_messages'] = Message.objects.filter(conversation=context['conversation'])
        return context

class ConversationCreate(LoginRequiredMixin, CreateView):
    model = Conversation
    fields = '__all__'
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(ConversationCreate, self).get_context_data(**kwargs)
        # Only show only groups that this user is a member of
        context['form'].fields['group'].queryset = Group.objects.filter(users__pk = self.request.user.pk)
        return context
    def get_success_url(self):
        return reverse_lazy('conversations:conversation-detail', kwargs = {'pk' : self.object.pk})

class ConversationUpdate(LoginRequiredMixin, UpdateView):
    model = Conversation
    fields = ['subject']
    def get_success_url(self):
        return reverse_lazy('conversations:conversation-detail', kwargs = {'pk' : self.object.pk})

class ConversationDelete(LoginRequiredMixin, DeleteView):
    template_name = 'conversations/delete_confirm.html'
    model = Conversation
    success_url = reverse_lazy('conversations:conversation-list')
    def get_context_data(self, **kwargs):
        # Check that the conversation exists and the user is a member of the group
        get_object_or_404(Conversation, pk = self.object.pk, group__users__pk = self.request.user.pk)
        # Call the base implementation first to get a context
        context = super(ConversationDelete, self).get_context_data(**kwargs)
        return context

class MessageCreate(LoginRequiredMixin, CreateView):
    model = Message
    fields = ['text']
    def form_valid(self, form):
        form.instance.user = User.objects.get(pk = self.request.user.pk)
        form.instance.conversation = Conversation.objects.get(pk = self.kwargs['pk'])
        return super(CreateView, self).form_valid(form)
        
    def get_success_url(self):
        return reverse_lazy('conversations:conversation-detail', kwargs = {'pk' : Conversation.objects.get(pk = self.object.conversation.pk).pk})

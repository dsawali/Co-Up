from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.core.paginator import Paginator
from django.shortcuts import render,\
                             redirect,\
                             get_object_or_404

from .forms import PositionForm, CommentForm
from .models import Position, Comment
from coup.users.models import User
# Create your views here.

LOGIN_URL = '/login/'


class PositionListView(LoginRequiredMixin,\
                           generic.ListView):
    """
    Lists the positions of the user which 
    is currently logged in
    """
    login_url = LOGIN_URL
    paginate_by = 2
    template_name = 'positions/position_overview.html'
    model = Position

    def get_queryset(self):
        return Position.objects.filter(user=self.request.user)
    

class PositionOverview(LoginRequiredMixin,\
                       generic.ListView):
    """
    Displays the dashboard of the app.
    """
    login_url = LOGIN_URL
    model = User
    template_name = 'positions/index.html'

    def get_context_data(self, **kwargs):
        context = super(PositionOverview, self).get_context_data(**kwargs)
        context['recommended_list'] = Position.objects.filter(\
            user__faculty=self.request.user.faculty).order_by('-id')[0:5]
        context['recent_list'] = Position.objects.exclude(\
                                    user=self.request.user).order_by('-id')[0:5]
        context['position_list'] = Position.objects.filter(user=self.request.user)
        return context


class PositionDetailView(LoginRequiredMixin,\
                         generic.DetailView):
    """
    Generic view to display details of a specific position.
    """
    login_url = LOGIN_URL
    model = Position


@login_required(login_url = LOGIN_URL)
def add_position(request):
    """
    view generates the template to add a new position
    and comment and awaits a POST request by the user.
    """
    if request.method == "POST":
        form1 = PositionForm(request.POST)
        form2 = CommentForm(request.POST)
        if (form1.is_valid() & form2.is_valid()):
            position = form1.save(commit=False)
            if position.location_addr is not None:
                if position.company in position.location_addr:
                    new_addr = position.location_addr.split(',')[1:]
                    position.location_addr = ','.join(new_addr)
            position.user = request.user
            position.generate_slug()
            position.save()
            comment = form2.save(commit=False)
            comment.position = position
            comment.user = request.user
            comment.save()
            return redirect('positions:position-detail',\
                pk=position.pk,\
                slug=position.slug) 
    else:
        form1 = PositionForm()
        form2 = CommentForm()
    return render(request, 'positions/position_add.html',{'form1':form1, 'form2':form2})


@login_required(login_url = LOGIN_URL)
def edit_position(request, *args, **kwargs):
    """
    Enables the user to edit a position added to the DB
    in case an error was recorded.
    """
    pk = kwargs['pk'][0]
    position = get_object_or_404(Position, pk=pk)
    comment = Comment.objects.get(position=pk)
    
    if request.user != position.user:
        return HttpResponseRedirect('/user_auth/error')

    if request.method == "POST":
        form1 = PositionForm(request.POST, instance=position)
        form2 = CommentForm(request.POST, instance=comment)
        if (form1.is_valid() & form2.is_valid()):
            position = form1.save(commit=False)
            if position.company in position.location_addr:
                new_addr = position.location_addr.split(',')[1:]
                position.location_addr = ','.join(new_addr)
            position.save()
            comment = form2.save(commit=False)
            comment.save()
            return redirect('positions:position-detail',\
                pk=position.pk,\
                slug=position.slug)
    else:
        form1 = PositionForm(instance=position)
        form2 = CommentForm(instance=comment)
    return render(request, 'positions/position_edit.html', {'form1':form1, 'form2':form2})


@login_required(login_url = LOGIN_URL)
def delete_position(request, *args, **kwargs):
    """
    Enables the user to delete a position they have posted to
    the database
    """
    position = get_object_or_404(Position, **kwargs).delete()
    return redirect('positions:index') 

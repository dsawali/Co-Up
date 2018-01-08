from django.shortcuts import render
from django.views.generic import ListView
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin

from coup.positions.models import Position, Comment
from coup.users.models import User

LOGIN_URL = '/login/'

def recommend_user(self):
        
    
    rec_users = user_objects.filter(Q(faculty="Sciences")\
                                             | Q(program="Computing Science"))
    return rec_users
    
class DashBoardView(LoginRequiredMixin,\
                    ListView):
    """
    Generic view used to render the homepage aka
    dashboard of the website.
    """
    login_url = LOGIN_URL
    model = User
    template_name = "dashboard/index.html"

    def get_context_data(self, **kwargs):
        context = super(DashBoardView, self).get_context_data(**kwargs)
        #context['recent_list'] = Position.objects.exclude(\
         #                           user=self.request.user).order_by('-id')
        
        """user_objects = User.objects.exclude(id=self.request.user.id)
        rec_users = user_objects.filter(\
                                Q(faculty=self.request.user.faculty) | \
                                Q(program=self.request.user.program))

        context['recommend_users'] = rec_users"""
        return context


    


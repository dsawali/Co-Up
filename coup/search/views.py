from django.views.generic import ListView
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import UserSearchForm, PositionSearchForm
from ..positions.models import Position, Comment
from ..users.models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


LOGIN_URL = '/login/'

class SearchView(LoginRequiredMixin,\
                 ListView):
    """
    View to display search form for users / interview questions
    of specific positions.
    """
    login_url = LOGIN_URL
    model = Position 
    template_name = 'search/search.html'
    paginate_by = 2

    POSITION_KEY = 'company'
    USER_KEY = 'username'

    def get_context_data(self,\
                         *args,\
                         **kwargs):
        """
        Gets all relevant data for template context.
        """
        data = super(SearchView, self).\
            get_context_data(**self.request.GET)
        data['positions_form'] = PositionSearchForm
        data['users_form'] = UserSearchForm
        return data
        
    def get_queryset(self,
                     **kwargs):
        """
        Performs filtering of positions based on GET parameters.
        """
        if self.POSITION_KEY in self.request.GET:
            positions_l = Position.objects.\
                query_on_params(**self.request.GET)
            return positions_l

        elif self.USER_KEY in self.request.GET:
            users_l = User.objects.\
                query_on_params(**self.request.GET)
            return users_l

        else:
            return []
    

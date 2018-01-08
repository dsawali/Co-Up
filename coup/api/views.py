from django.shortcuts import render
from django.http import HttpResponse
from django.db.models import Q

from ..positions.models import Position
from ..users.models import User

import json


def get_generic_val(request,
                    cb_filter,
                    *args):
    """
    Generic API to be wrapped to 
    query specific database fields 
    based on user input.     
    """
    content_type = 'application/json'

    if request.is_ajax():
        term_s = request.GET['term'][0]
        object_l = cb_filter(term_s)
        delimeter = ' '

        match_l = []    
        dup_d = {}
        for obj in object_l:
            field_l = []  
            for field in args:
                field_l.append(\
                    obj.__dict__[field])
            match = delimeter.join(field_l)
            if match not in dup_d:
                match_l.append(\
                    match)
                dup_d[match] = 1
        
        data = json.dumps(match_l)

    else:
        data = 'fail'

    return HttpResponse(data,\
        content_type = content_type) 

def position_title_wrapper(title_s):
    """
    Wraps the Position.objects.filter
    method on title__icontains kwarg.
    """
    return Position.objects.filter(\
        title__icontains = title_s)

def position_company_wrapper(company_s):
    """
    Wraps the Position.objects.filter
    method on company__icontains kwarg.
    """
    return Position.objects.filter(\
        company__icontains = company_s)

def user_username_wrapper(username_s):
    """
    Wraps the User.objects.filter
    method on username__icontains kwarg.
    """
    return User.objects.filter(\
        username__icontains = username_s)

def user_fullname_wrapper(fullname_s):
    """
    Wraps the User.objects.filter
    method on first_name__icontains
    and last_name__icontains kwargs.
    """
    name_l = fullname_s.split(' ')
    try:
        return User.objects.filter(\
            first_name__icontains = name_l[0],\
            last_name__icontains = name_l[1])        

    except IndexError:        
        return User.objects.filter(\
            Q(first_name__icontains = name_l[0]) |\
            Q(last_name__icontains = name_l[0]))

def get_titles(request):
    """
    Queries for positions starting with input 
    contained within GET request.
    """
    return get_generic_val(request,\
        position_title_wrapper,\
        'title') 

def get_companies(request):
    """
    Queries for company names starting 
    with input contained within GET request.
    """
    return get_generic_val(request,\
        position_company_wrapper,\
        'company') 

def get_usernames(request):
    """
    Queries for usernames starting with input
    contained within GET request.
    """
    return get_generic_val(request,\
        user_username_wrapper,\
        'username')        

def get_fullnames(request):
    """
    Queries for first/last names starting with input
    contained within GET request.
    """
    return get_generic_val(request,\
        user_fullname_wrapper,\
        'first_name',
        'last_name')        



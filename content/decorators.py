from django.http import HttpResponse
from django.shortcuts import redirect

def authenticated_user(view_func):
    def container(request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponse('You are not authorized to view this page.\n Logout first.')
            
        else:
            return view_func(request, *args, **kwargs)
    return container

def unauthenticated_user(view_func):
    def container(request, *args, **kwargs):
        if request.user.is_anonymous:
            return HttpResponse('You are not authorized to view this page.\n Login first.')
            
        else:
            return view_func(request, *args, **kwargs)
    return container
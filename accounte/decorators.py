from django.http import HttpResponse
from django.shortcuts import redirect, render

def unauthenticated_user(view_fun): 
    def wrap_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('dashboard')
        else:
            return view_fun(request, *args, **kwargs)
    return wrap_func

def allowed_users(allowed_roles=[]):
    def decorators(view_func):
        def wrap_func(request, *args, **kwargs):
            group = None
            if request.user.groups.exists():
                group =  request.user.groups.all()[0].name
            if group in allowed_roles:
                return view_func(request, *args, **kwargs)
            else:
                return HttpResponse('youre not authorised to view this page')
        return wrap_func
    return decorators


def admin_only(view_func):
    def wrap_func(request, *args, **kwargs):
        group = None
        if request.user.groups.exists():
            group =  request.user.groups.all()[0].name
        if group == 'admin':
            return view_func(request, *args, **kwargs)
        if group == 'customer':
            return redirect('userpage')
    return wrap_func
        
        
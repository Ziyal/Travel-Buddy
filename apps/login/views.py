from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from .models import User

def index(request):
    return render(request, 'login/index.html')

def register(request):
    response_from_models = User.objects.register_user(request.POST)
    if response_from_models['status']:
        request.session['user_id'] = response_from_models['user'].id
        request.session['name'] = response_from_models['user'].name
        return redirect('project:index')
    else:
        for error in response_from_models['errors']:
            messages.error(request, error)
            return redirect('/')

def login(request):

    response_from_models = User.objects.login_user(request.POST)

    if response_from_models['status']:
        request.session['user_id'] = response_from_models['user'].id
        request.session['name'] = response_from_models['user'].name
        return redirect('project:index')
    else:
        for error in response_from_models['errors']:
            messages.error(request, error)
        return redirect('login:index')

def success(request):
    if not "user_id" in request.session:
        messages.error(request, "Must be logged in to view this page")
        return redirect('login:index')
    return render(request, "project:index")

def logout(request):
    request.session.clear()
    return redirect('login:index')

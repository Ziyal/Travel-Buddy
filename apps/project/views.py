from django.shortcuts import render, redirect
from ..login.models import User
from .models import Trip
from django.contrib import messages

def index(request):
    if not "user_id" in request.session:
        messages.error(request, "Must be logged in to view this page")
        return redirect('login:index')

    current_user = User.objects.get(id=request.session['user_id'])
    context = {
        "users": User.objects.all(),
        "trips": Trip.objects.all(),
        "created_by_me": Trip.objects.filter(creator=current_user)|Trip.objects.filter(buddy=current_user).order_by("date_from"),
        "created_by_other": Trip.objects.all().exclude(creator=current_user).exclude(buddy=current_user).order_by("date_from"),
    }
    return render(request, 'project/index.html', context)

def trip(request, id):
    if not "user_id" in request.session:
        messages.error(request, "Must be logged in to view this page")
        return redirect('login:index')

    current_user = Trip.objects.get(id=request.session['user_id'])
    context = {
        "trips": Trip.objects.get(id=id),
        "trip_creator": Trip.objects.filter(id=id),
        "buddy_trip": User.objects.filter(buddy__id=id)
    }
    return render(request, 'project/trip.html', context)

def add_travel_plan(request):
    return render(request, 'project/new_trip.html')

def process_trip(request):
    if request.method == "POST":
        response_from_models = Trip.objects.create_trip(request.POST, request.session['user_id'])

        if response_from_models['status']:
            return redirect('project:index')
        else:
            for error in response_from_models['errors']:
                messages.error(request, error)
            return redirect('project:add_travel_plan')

def join(request, id):
    current_user = User.objects.get(id = request.session['user_id'])
    current_trip = Trip.objects.get(id=id)
    current_trip.buddy.add(current_user)
    current_trip.save()
    return redirect('project:index')

def logout(request):
    request.session.clear()
    return redirect('login:index')

from __future__ import unicode_literals
from django.db import models
from ..login.models import User
import datetime

class TripManager(models.Manager):
    def create_trip(self, postData, user_id):
        errors = []
        response_to_views = {}
        current_date = str(datetime.date.today())

        if not len(postData['destination']):
            errors.append('Destination must not be blank')
        if not len(postData['description']):
            errors.append('Description must not be blank')
        if postData['date_from'] < current_date:
            errors.append('Date From must be in the future')
        if postData['date_to'] < postData['date_from']:
            errors.append('"Date To" must be after "Date From"')
        if not errors:
            add_trip = Trip.objects.create(destination=postData['destination'], description=postData['description'], date_from=postData['date_from'], date_to=postData['date_to'], creator=User.objects.get(id=user_id))
            print "*"*50
            print add_trip.destination
            response_to_views['add_trip'] = add_trip
            response_to_views['status'] = True
        else:
            response_to_views['errors'] = errors
            response_to_views['status'] = False
        return response_to_views

class Trip(models.Model):
    destination = models.CharField(max_length=100)
    description = models.CharField(max_length=150)
    date_from = models.DateField(max_length=100)
    date_to = models.DateField(auto_now_add = False)
    buddy = models.ManyToManyField(User, related_name='buddy')
    creator = models.ForeignKey(User, related_name='creator')
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    objects = TripManager()

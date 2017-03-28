from __future__ import unicode_literals
from django.db import models
import re, bcrypt
import datetime
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class UserManager(models.Manager):
    def register_user(self, postData):
        errors = []

        if len(postData['name']) < 3:
            errors.append('First name must be longer than 3 characters')
        if len(postData['username']) < 3:
            errors.append('Username must be longer than 3 characters')
        if len(postData['password']) < 8:
            errors.append('Password must be at least 8 characters')
        if not postData['password'] == postData['password_cf']:
            errors.append('Password must match')
        user = User.objects.filter(username=postData['username'])
        if user:
            errors.append("Username has already been used")

        response_to_views = {}

        if not errors:
            hashed_password = bcrypt.hashpw(postData['password'].encode(), bcrypt.gensalt())
            user = User.objects.create(name = postData['name'], username = postData['username'], password = hashed_password)
            response_to_views['user'] = user
            response_to_views['status'] = True

        else:
            response_to_views['errors'] = errors
            response_to_views['status'] = False
        return response_to_views

    def login_user(self, postData):
        response_to_views = {}
        errors = []

        user = self.filter(username = postData['username'])
        if not user:
            errors.append('Invalid username')
            response_to_views['errors'] = errors
            response_to_views['status'] = False

        else:
            if bcrypt.checkpw(postData['password'].encode(), user[0].password.encode()):
                response_to_views['status'] = True
                response_to_views['user'] = user.first()
            else:
                errors.append('Invalid email/password')
                response_to_views['errors'] = errors
                response_to_views['status'] = False
        return response_to_views


# **********************************************
class User(models.Model):
    name = models.CharField(max_length=100)
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    objects = UserManager()

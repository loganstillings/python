from __future__ import unicode_literals
from django.db import models
import re, bcrypt
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
# Create your models here.
class UserManager(models.Manager):
    def add_user(self, postData):
        errors = []
        if len(postData['first_name']) < 2:
            errors.append('First name must be at least 2 characters long')
        if len(postData['last_name']) < 2:
            errors.append('Last name must be at least 2 characters long')
        if not postData['email']:
            errors.append('Email is required')
        if not EMAIL_REGEX.match(postData['email']):
            errors.append('Email is invalid')
        check_email = self.filter(email=postData['email'])
        if check_email:
            errors.append('Email already exists in database')
        if not postData['password']:
            errors.append('Password is required')
        if len(postData['password']) < 8:
            errors.append('Password must be at least 8 characters')
        if not postData['password'] == postData['password_confirm']:
            errors.append('Password fields must match')

        modelsResponse = {}

        if errors:
            modelsResponse['isRegistered'] = False
            modelsResponse['errors'] = errors
        else:
            modelsResponse['isRegistered'] = True
            hashed_password = bcrypt.hashpw(postData['password'].encode(), bcrypt.gensalt())
            user = self.create(first_name=postData['first_name'], last_name=postData['last_name'], email=postData['email'], password=hashed_password)
            modelsResponse['user'] = user

        return modelsResponse

    def login_user(self, postData):
        user = self.filter(email= postData['email'])
        errors = []
        models2Response = {}
        if not user:
            errors.append('Email not in database')
        else:
            if bcrypt.checkpw(postData['password'].encode(), user[0].password.encode()):
                models2Response['isLoggedIn'] = True
                models2Response['user'] = user[0]
            else:
                errors.append('Invalid email/password combination')
        if errors:
            models2Response['isLoggedIn'] = False
            models2Response['errors'] = errors

        return models2Response

class User(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=300)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    objects = UserManager()

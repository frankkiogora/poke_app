from __future__ import unicode_literals
import re
import bcrypt
from django.db import models
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]*$')
NAME_REGEX = re.compile(r'^[A-Za-z]\w+$')

class UserManager(models.Manager):
    def register_validate(self, postData):
        errors = []

        first_name = postData['first_name']
        last_name = postData['last_name']
        alias = postData['alias']
        email = postData['email'].lower()
        birthday= postData['birthday']
        password = postData['password']
        cpassword = postData['cpassword']

        if not first_name or not last_name or not email or not birthday or not password or not cpassword:
            errors.append( "All fields are required")

        # check name
        if len(first_name) < 3 or len(last_name) < 3:
            errors.append( "name fields should be at least 3 characters")
        elif not NAME_REGEX.match(first_name) or not NAME_REGEX.match(last_name):
            errors.append( "name is not valid")

        # check email
        if len(email) < 1:
            errors.append( "Email cannot be blank")
        elif not EMAIL_REGEX.match(email):
            errors.append( "Email is not valid")

        if len(birthday) <1:
			errors.append('Please enter birthday')


        # check password
        if len(password ) < 8:
            errors.append ( "password must be at least 8 characters")
        elif password != cpassword:
            errors.append ( "password must be match")

        if not errors:
            if User.objects.filter(email=email):
                errors.append("email is not unique")
            else:
                hashed = bcrypt.hashpw((password.encode()), bcrypt.gensalt(5))

                return self.create(
                    first_name= first_name,
                    last_name =last_name,
                    alias=alias,
                    email=email,
                    birthday=birthday,
                    password=hashed
                )

        return errors

    def login_validate(self, postData):
        errors = []
        password = postData['password']
        email = postData['email']
                # check DB for email
        try:
            # check user's password
            user = self.get(email=email)
            if bcrypt.checkpw(password.encode(), user.password.encode()):
                return user

        except:
            pass

        errors.append('Invalid login info')
        return errors


class User(models.Model):
      first_name = models.CharField(max_length=255, default="")
      last_name = models.CharField(max_length=255, default="")
      alias = models.CharField(max_length=255)
      email = models.CharField(max_length=255)
      birthday=models.CharField(max_length=10)
      password = models.CharField(max_length=255)
      created_at = models.DateTimeField(auto_now_add = True)
      updated_at = models.DateTimeField(auto_now = True)
      objects = UserManager()

class Poke(models.Model):
    poker = models.ForeignKey(User, related_name="poking")
    poked_by = models.ForeignKey(User, related_name="poked")
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

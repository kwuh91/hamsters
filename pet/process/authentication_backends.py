from django.contrib.auth.backends import ModelBackend
from .models import Worker
from django.contrib.auth import get_user_model
from django.contrib.auth.signals import user_logged_out
from django.contrib.auth.models import User
from django.conf import settings
from django.contrib.auth.backends import BaseBackend

# class WorkerAuthBackend(ModelBackend):
#     def authenticate(self, request, username=None, password=None, **kwargs):
#         try:
#             worker = Worker.objects.get(login=username, password=password)
#         except Worker.DoesNotExist:
#             return None  # Return None if no worker with the given credentials is found

        

#         return worker  # Return the worker if credentials are valid


class WorkerAuthBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        user_valid = Worker.objects.filter(login=username, password=password).exists() 
        user_is_admin = settings.ADMIN_LOGIN == username and settings.ADMIN_PASSWORD == password

        if user_valid:
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                # Create a user if it doesn't exist
                    user = User(username=username)
                    user.is_superuser = True if user_is_admin else False
                    user.is_staff = False if user_is_admin else True
                    user.save()

            return user
        return None 


def get_user(self, user_id):
    try:
        return User.objects.get(pk=user_id)
    except User.DoesNotExist:
        return None
        
from django.contrib.auth.backends import ModelBackend
from .models import Worker 

class WorkerAuthBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            worker = Worker.objects.get(login=username, password=password)
        except Worker.DoesNotExist:
            return None  # Return None if no worker with the given credentials is found

        return worker  # Return the worker if credentials are valid

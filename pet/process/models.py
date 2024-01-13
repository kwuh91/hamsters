from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

# Create your models here.

class Image(models.Model):
    image = models.ImageField(upload_to='images/')
    animal_type = models.CharField(max_length=255)


class Service(models.Model):
    name = models.CharField(max_length=255)
    price = models.IntegerField()
    animal_type = models.CharField(max_length=255)


class Salon(models.Model):
    address = models.CharField(max_length=255)


class Client(models.Model):
    name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=11)  # Adjust max_length as needed
    email = models.EmailField()


class WorkerManager(BaseUserManager):
    def create_user(self, login, password=None, **extra_fields):
        user = self.model(login=login, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, login, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(login, password, **extra_fields)


class Worker(AbstractBaseUser, PermissionsMixin):
    login = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = WorkerManager()

    USERNAME_FIELD = 'login'

    # Add related_name to avoid clashes
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='worker_groups',
        blank=True,
        verbose_name='groups',
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='worker_user_permissions',
        blank=True,
        verbose_name='user permissions',
        help_text='Specific permissions for this user.',
    )

    # def __str__(self):
    #     return self.login


# class User(models.Model):
#     worker = models.OneToOneField(Worker, on_delete=models.CASCADE)


class Cart(models.Model):
    price = models.IntegerField()
    quantity = models.IntegerField()


class OrdersHistory(models.Model):
    staff_login = models.CharField(max_length=255)

    client_name = models.CharField(max_length=255)
    client_email = models.EmailField()
    client_phone_number = models.CharField(max_length=11)  # Adjust max_length as needed

    salon_address = models.CharField(max_length=255)

    price = models.IntegerField()

    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.input_text

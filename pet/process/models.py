from django.db import models

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

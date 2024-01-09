from django.shortcuts import render, redirect
from django.http import HttpResponseNotFound
from typing import Any
from .models import Image, Service, Salon, Client, Worker
from django.utils import timezone
from django.http import JsonResponse
from typing import Any
from rest_framework import generics
from django.contrib.auth import authenticate, login

# Create your views here.

# homepage
def index(request):
    return render(request, 'process/authorization.html')


# authorization 
def process(request):
    username: Any
    password: Any

    # get login and password 
    if request.method == 'POST':
        # Redirect to the next page after successful login
        next_url = request.POST.get('next', None)
        if next_url:
            return redirect(next_url)

        # Get the values from the form
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        print(f"Login: {username}, Password: {password}")

    # get new client data
    else:
        client_name = request.GET.get("newClientName")
        client_phone = request.GET.get("newClientPhone")
        client_email = request.GET.get("newClientEmail")

        print(f"Name: {client_name}, Phone: {client_phone}, Email: {client_email}")

        Client.objects.create(name=client_name, phone_number=client_phone, email=client_email)
        
    # return render to admin/worker page
    if user is not None and user.is_active:
            login(request, user)

            if user.is_superuser:
                # adminpage
                images = Image.objects.all()
                return render(request, 'process/adminpage.html', {'animals': images})
            
            elif user.is_staff:
                # workerpage
                images = Image.objects.all()
                salons = Salon.objects.all()
                clients = Client.objects.all()
                return render(request, 'process/workerpage.html', {'images': images, 'salons': salons, 'clients': clients})

    # Invalid login credentials
    return render(request, 'process/authorization.html', {'error_message': 'Invalid login credentials.'})
    

# get the price
def current_price(request):        
    return HttpResponseNotFound("<h1>Page not found</h1>")


# upload new image of an animal to a database 
def upload_image(request):
    images = Image.objects.all()
    if request.method == 'POST':
        # Get the values from the form
        image_file = request.FILES.get('image')
        animal_type = request.POST.get('animal_type')

        if image_file:
            # check if this animal_type already present in process_image table
            existing_object = Image.objects.filter(animal_type=animal_type).first()
            if not existing_object:
                Image.objects.create(image=image_file, animal_type=animal_type)
                return render(request, 'process/adminpage.html', {'animals': images})
            else:
                # animal already exists
                return render(request, 'process/adminpage.html', {'error_message': 'Animal already exists.', 'animals': images})
        else:
            # error uploading image
            return render(request, 'process/adminpage.html', {'error_message': 'Error while uploading image.', 'animals': images})
        
    return render(request, 'process/adminpage.html', {'error_message': 'Error while retrieving data.', 'animals': images})


# add new service to a database
def add_service(request):
    images = Image.objects.all()
    if request.method == 'POST':
        # Get the values from the form
        price = request.POST.get('price_input')
        service_name = request.POST.get('service_name')
        animal_type = request.POST.get('animaldropdown')

        # check if this animal_type already present in process_service table
        existing_object = Service.objects.filter(name=service_name).first()
        if not existing_object:
            Service.objects.create(name=service_name, price=price, animal_type=animal_type)

            return render(request, 'process/adminpage.html', {'animals': images})
        else:
            # Service already exists
            return render(request, 'process/adminpage.html', {'error_message': 'Service already exists.', 'animals': images})
        
    return render(request, 'process/adminpage.html', {'error_message': 'Error while retrieving data.', 'animals': images})


# add new worker to a database
def add_worker(request):
    images = Image.objects.all()
    if request.method == 'POST':
        # Get the values from the form
        staff_login = request.POST.get('staff_login')
        staff_password = request.POST.get('staff_password')
        
        # check if this staff_login already present in process_worker table
        existing_object = Worker.objects.filter(login=staff_login).first()
        if not existing_object:
            Worker.objects.create(login=staff_login, password=staff_password, is_active=1, is_staff=1, is_superuser=0)

            return render(request, 'process/adminpage.html', {'animals': images})
        else:
            # Login already exists
            return render(request, 'process/adminpage.html', {'error_message': 'Such login already exists.', 'animals': images})
        
    return render(request, 'process/adminpage.html', {'error_message': 'Error while retrieving data.', 'animals': images})


# fetch services for a specific image
def get_services_for_image(request, animal_type):
    services = Service.objects.filter(animal_type=animal_type).values('name', 'price')
    return JsonResponse({'services': list(services)})


# fetch client data
def save_client(request):
    if request.method == 'POST':
        # Retrieve form data from the AJAX request
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        email = request.POST.get('email')

        # Perform saving logic (replace with your actual saving logic)
        # Example: Create a new client instance and save it
        Client.objects.create(name=name, phone_number=phone, email=email)
        # new_client = Client(name=name, phone=phone, email=email)
        # new_client.save()

        # Return a JSON response indicating success
        return JsonResponse({'message': 'Client saved successfully'})

    # Return a JSON response indicating failure (in case of GET request)
    return JsonResponse({'error': 'Invalid request method'})


def dummy_view(request):
    images = Image.objects.all()
    return render(request, 'process/adminpage.html', {'error_message': 'dummy view.'})

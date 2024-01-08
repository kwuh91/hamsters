from django.shortcuts import render, redirect
from django.http import HttpResponseNotFound
from typing import Any
from .models import Image, Service, Salon, Client
from django.utils import timezone
from django.http import JsonResponse
from typing import Any
from rest_framework import generics

# Create your views here.

# homepage
def index(request):
    return render(request, 'process/authorization.html')


# authorization 
def process(request):
    login: Any
    password: Any

    # get login and password 
    if request.method == 'POST':
        # Get the values from the form
        login = request.POST.get('username')
        password = request.POST.get('password')

        print(f"Login: {login}, Password: {password}")

    # get new client data
    else:
        client_name = request.GET.get("newClientName")
        client_phone = request.GET.get("newClientPhone")
        client_email = request.GET.get("newClientEmail")

        print(f"Name: {client_name}, Phone: {client_phone}, Emial: {client_email}")

        Client.objects.create(name=client_name, phone_number=client_phone, email=client_email)
    
    # return render to admin/worker page
    if login == 'admin' and password == 'admin':
        return render(request, 'process/adminpage.html')
    else:
        # workerpage
        images = Image.objects.all()
        salons = Salon.objects.all()
        clients = Client.objects.all()
        return render(request, 'process/workerpage.html', {'images': images, 'salons': salons, 'clients': clients})
    

# get the price
def current_price(request):        
    if request.method == 'POST':
        # Get the values from the form
        salon = request.POST.get('salon')
        client = request.POST.get('salon')

        print(f"Login: {salon}, Password: {client}")

    return HttpResponseNotFound("<h1>Page not found</h1>")


# upload new image of an animal to a database 
def upload_image(request):
    if request.method == 'POST':
        # Get the values from the form
        image_file = request.FILES.get('image')
        animal_type = request.POST.get('animal_type')
        price = request.POST.get('price_input')
        service_name = request.POST.get('service_name')

        if image_file:
            # check if this animal_type already present in process_image table
            existing_object = Image.objects.filter(animal_type=animal_type).first()
            if not existing_object:
                Image.objects.create(image=image_file, animal_type=animal_type)

            Service.objects.create(name=service_name, price=price, animal_type=animal_type)
            return redirect('upload_image')  # Redirect to the gallery page or any other page
        
    return render(request, 'process/adminpage.html')


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
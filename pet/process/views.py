from django.shortcuts import render, redirect
from django.http import HttpResponseNotFound
from typing import Any
from .models import Image, Service, Salon, Client, Worker, Cart, OrdersHistory
from django.utils import timezone
from django.http import JsonResponse
from typing import Any
from rest_framework import generics
from django.contrib.auth import authenticate, login
import numpy as np

# Create your views here.

# homepage
def index(request):
    return render(request, 'process/authorization.html')


# authorization 
def process(request):
    username: Any
    password: Any
    is_redirect = False

    # get login and password 
    if request.method == 'POST':
        # Redirect to the next page after successful login
        # next_url = request.POST.get('next', None)
        # if next_url:
        #     return redirect(next_url)

        # Get the values from the form
        username = request.POST.get('username')
        password = request.POST.get('password')

        if username is None and password is None:
            is_redirect = True

        user = authenticate(request, 
                            username=username, 
                            password=password) if not is_redirect else request.user

        print(f"Login: {username}, Password: {password}")

        # return render to admin/worker page
        if user is not None:
            if not is_redirect:
                login(request, user)

            clients = Client.objects.all()
            images  = Image.objects.all()

            if user.is_superuser:
                # adminpage
                workers = Worker.objects.all()
                return render(request, 'process/adminpage.html', {'animals' : images, 
                                                                  'clients' : clients,
                                                                  'workers' : workers})
            
            elif user.is_staff:
                # workerpage
                salons  = Salon.objects.all()
                return render(request, 'process/workerpage.html', {'images' : images, 
                                                                   'salons' : salons, 
                                                                   'clients': clients})

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
        image_file  = request.FILES.get('image')
        animal_type = request.POST.get('animal_type')

        if image_file:
            # check if this animal_type already present in process_image table
            existing_object = Image.objects.filter(animal_type=animal_type).first()
            if not existing_object:
                Image.objects.create(image=image_file, 
                                     animal_type=animal_type)
                return render(request, 'process/adminpage.html', {'animals': images})
            else:
                # animal already exists
                return render(request, 'process/adminpage.html', {'error_message': 'Animal already exists.', 
                                                                  'animals'      : images})
        else:
            # error uploading image
            return render(request, 'process/adminpage.html', {'error_message': 'Error while uploading image.', 
                                                              'animals'      : images})
        
    return render(request, 'process/adminpage.html', {'error_message': 'Error while retrieving data.', 
                                                      'animals'      : images})


# add new service to a database
def add_service(request):
    images = Image.objects.all()
    if request.method == 'POST':
        # Get the values from the form
        price        = request.POST.get('price_input')
        service_name = request.POST.get('service_name')
        animal_type  = request.POST.get('animaldropdown')

        # check if this animal_type already present in process_service table
        existing_object = Service.objects.filter(name=service_name).first()
        if not existing_object:
            Service.objects.create(name=service_name, 
                                   price=price, 
                                   animal_type=animal_type)

            return render(request, 'process/adminpage.html', {'animals': images})
        else:
            # Service already exists
            return render(request, 'process/adminpage.html', {'error_message': 'Service already exists.', 
                                                              'animals'      : images})
        
    return render(request, 'process/adminpage.html', {'error_message': 'Error while retrieving data.', 
                                                      'animals'      : images})


# add new worker to a database
def add_worker(request):
    images = Image.objects.all()
    if request.method == 'POST':
        # Get the values from the form
        staff_login    = request.POST.get('staff_login')
        staff_password = request.POST.get('staff_password')
        
        # check if this staff_login already present in process_worker table
        existing_object = Worker.objects.filter(login=staff_login).first()
        if not existing_object:
            Worker.objects.create(login=staff_login, 
                                  password=staff_password, 
                                  is_active=1, 
                                  is_staff=1, 
                                  is_superuser=0)

            return render(request, 'process/adminpage.html', {'animals': images})
        else:
            # Login already exists
            return render(request, 'process/adminpage.html', {'error_message': 'Such login already exists.', 
                                                              'animals'      : images})
        
    return render(request, 'process/adminpage.html', {'error_message': 'Error while retrieving data.', 
                                                      'animals'      : images})


# fetch orders
def get_orders(request):
    login  = request.POST.get('login')
    client_id = request.POST.get('client')
    client_name  = Client.objects.get(id=client_id).name
    client_phone = Client.objects.get(id=client_id).phone_number
    client_email = Client.objects.get(id=client_id).email

    orders = OrdersHistory.objects.filter(staff_login=login, 
                                    client_name=client_name, 
                                    client_email=client_email, 
                                    client_phone_number=client_phone).values('price', 
                                                                             'timestamp',
                                                                             'id')
    return JsonResponse({'orders': list(orders)})


# fetch services for a specific image
def get_services_for_image(request, animal_type):
    services = Service.objects.filter(animal_type=animal_type).values('name', 
                                                                      'price', 
                                                                      'id', 
                                                                      'animal_type')
    return JsonResponse({'services': list(services)})


# fetch client data
def save_client(request):
    if request.method == 'POST':
        # Retrieve form data from the AJAX request
        name  = request.POST.get('name')
        phone = request.POST.get('phone')
        email = request.POST.get('email')

        # Perform saving logic (replace with your actual saving logic)
        # Example: Create a new client instance and save it
        Client.objects.create(name=name, 
                              phone_number=phone, 
                              email=email)
        # new_client = Client(name=name, phone=phone, email=email)
        # new_client.save()

        # Return a JSON response indicating success
        return JsonResponse({'message': 'Client saved successfully'})

    # Return a JSON response indicating failure (in case of GET request)
    return JsonResponse({'error': 'Invalid request method'})


def update_cart(request):
    if request.method == 'POST':
        print(request.POST)
        # print("Update")
        animal_type = request.POST.get('animal_type')
        services_with_current_animal_type = Service.objects.filter(animal_type=animal_type)
        list_of_ids = services_with_current_animal_type.values_list('id', flat=True)

        # Extracting data from the hidden input fields
        for id in list_of_ids:
            service_count = request.POST.get(f'service_count{id}')
            
            if service_count is not None:
                service_price = Service.objects.get(id=id).price
                Cart.objects.create(price=service_price, 
                                    quantity=int(service_count))
            
        # Return a JSON response indicating success
        return JsonResponse({'message': 'Cart updated successfully'})

    # Return a JSON response indicating failure (in case of GET request)
    return JsonResponse({'error': 'Invalid request method'})


def show_final_price(request):
    if request.method == 'POST':

        print("----------------------------------------------------------------------------------------------------------------------------------------------------")

        print(request.POST)

        cart = Cart.objects.all()
        final_price: int = 0
        for item in cart:
            final_price += item.price * item.quantity
        
        staff_login = request.user.username
        
        client_id     = request.POST.get('client')
        client_name  = Client.objects.get(id=client_id).name
        client_phone = Client.objects.get(id=client_id).phone_number
        client_email = Client.objects.get(id=client_id).email

        salon_id = request.POST.get('salon')
        salon_address = Salon.objects.get(id=salon_id).address

        print(f"final price = {final_price}")

        OrdersHistory.objects.create(staff_login=staff_login, 
                                    client_name=client_name, 
                                    client_phone_number=client_phone, 
                                    client_email=client_email, 
                                    salon_address=salon_address, 
                                    price=final_price, 
                                    timestamp=timezone.now())
        
        Cart.objects.all().delete()

        # Return a JSON response indicating success or not
        return JsonResponse({'final_price': final_price})
       
    # Return a JSON response indicating failure (in case of GET request)
    return JsonResponse({'error': 'An unexpected error occurred'})


def worker_history(request):
    history: Any
    wage: Any

    salons  = Salon.objects.all()
    clients = Client.objects.all()
    workers = Worker.objects.all()

    # admin
    if request.user.is_superuser:
        history = OrdersHistory.objects.all().order_by('-timestamp')
        wage = np.sum([obj.price for obj in history])
    # staff
    else:
        staff_login = request.user.username
        history = OrdersHistory.objects.filter(staff_login=staff_login).order_by('-timestamp')
        wage = np.sum([obj.price for obj in history])
    
    return render(request, 'process/worker_history.html', {'history'     : history, 
                                                           'wage_filter' : False, 
                                                           'wage'        : wage, 
                                                           'salons'      : salons, 
                                                           'clients'     : clients,
                                                           'admin'       : request.user.is_superuser,
                                                           'workers'     : workers})


def filter_history(request):
    if request.method == 'POST':
        history = OrdersHistory.objects.all()
        wage: Any

        salons  = Salon.objects.all()
        clients = Client.objects.all()
        workers = Worker.objects.all()

        # Retrieve form data
        sort_option = request.POST.get('sort_option')
        sort_by     = request.POST.get('sort_by')
        show_period = request.POST.get('show_period')
        start_date  = request.POST.get('start_date')
        end_date    = request.POST.get('end_date')

        client_id = request.POST.get('client')
        if bool(int(client_id)):
            client_name  = Client.objects.get(id=client_id).name
            client_phone = Client.objects.get(id=client_id).phone_number
            client_email = Client.objects.get(id=client_id).email

            history = history.filter(client_name=client_name, 
                                     client_phone_number=client_phone, 
                                     client_email=client_email)

        salon_id = request.POST.get('salon')
        if bool(int(salon_id)):
            salon_address = Salon.objects.get(id=salon_id).address

            history = history.filter(salon_address=salon_address)

        worker_id = request.POST.get('worker')
        if worker_id is not None and bool(int(worker_id)):
            worker_login = Worker.objects.get(id=worker_id).login

            history = history.filter(staff_login=worker_login)

        order_by_parameter: Any
        if sort_option is not None:
            order_by_parameter = '' if sort_option == 'asc' else '-'
        else:
            order_by_parameter = ''

        order_by_parameter += sort_by if sort_by is not None else 'timestamp'


        # admin
        if request.user.is_superuser:
            wage_filter = False
            if show_period is not None and bool(start_date) and bool(end_date) and start_date <= end_date:
                # print(f"start date: {bool(start_date)}")
                # print(f"end date: {end_date}")
                history = history.filter(timestamp__range=(start_date, end_date)).order_by(order_by_parameter)
                wage_filter = True
            else:
                history = history.order_by(order_by_parameter)

        # staff
        else:
            staff_login = request.user.username
            wage_filter = False
            if show_period is not None and start_date <= end_date:
                history = history.filter(staff_login=staff_login).filter(timestamp__range=(start_date, end_date)).order_by(order_by_parameter)
                wage_filter = True
            else:
                history = history.filter(staff_login=staff_login).order_by(order_by_parameter)

        wage = np.sum([obj.price for obj in history])
        return render(request, 'process/worker_history.html', {'history'     : history, 
                                                               'wage_filter' : wage_filter, 
                                                               'wage'        : wage, 
                                                               'salons'      : salons, 
                                                               'clients'     : clients,
                                                               'admin'       : request.user.is_superuser,
                                                               'workers'     : workers})


def delete_order(request):
    if request.method == 'POST':
        for item in request.POST:
            OrdersHistory.objects.filter(id=request.POST[item]).delete()

    return JsonResponse({'message': 'Cart updated successfully'})

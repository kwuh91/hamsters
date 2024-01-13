from django.urls import path
from . import views

# URLConf
urlpatterns = [
    path('', views.index, name='authorization'),
    path('process/', views.process, name='process'),
    path('current_price/', views.current_price, name='current_price'),
    path('upload_image/', views.upload_image, name='upload_image'),
    path('add_service/', views.add_service, name='add_service'),
    path('add_worker/', views.add_worker, name='add_worker'),
    path('get_services/<str:animal_type>/', views.get_services_for_image, name='get_services_for_image'),
    path('save-client/', views.save_client, name='save_client'),
    path('adminpage/', views.dummy_view, name='adminpage'),
    path('update_cart/', views.update_cart, name='update_cart'),
    path('show_final_price/', views.show_final_price, name='show_final_price'),
]

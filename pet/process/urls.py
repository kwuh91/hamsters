from django.urls import path
from . import views

# URLConf
urlpatterns = [
    path('', views.index, name='authorization'),
    path('process/', views.process, name='process'),
    path('current_price/', views.current_price, name='current_price'),
    path('upload_image/', views.upload_image, name='upload_image'),
    path('get_services/<str:animal_type>/', views.get_services_for_image, name='get_services_for_image'),
    path('save-client/', views.save_client, name='save_client'),
    # path('gallery/', views.image_gallery, name='image_gallery'),
]

from django.urls import path
from . import views


urlpatterns = [


    # path("", views.config, name=""),
    
    path("", views.main, name="main"),

    path("addpage/", views.addpage, name="addpage"),

   path('edit-device/<str:id_device>', views.edit_device, name="edit-device"),
   

   path("simple/<int:id_device>/", views.simple_queue, name="simple"),


   path("ping/<int:id_device>/", views.ping, name="ping"),

    # path("reboot/", views.reboot, name="reboot"),

    path("delete-device/<str:id_device>", views.delete_device, name="delete-device"),

    path("devices/", views.devices, name="devices"),

    path('config/<str:id_device>', views.config, name="config"),

    



]
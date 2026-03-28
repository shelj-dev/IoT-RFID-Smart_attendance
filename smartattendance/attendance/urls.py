from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('create_attendance/',views.create_attendance,name="create_attendance"),
    path('register_user/',views.register_user,name="register_user"),

    path('get-rfid/', views.get_rfid, name="get_rfid"),
    
    # api
    path('get-sensor/',views.get_sensor_data,name="get_sensor_data"),
    path('send-relay/',views.get_rfid_api,name="get_rfid_api"),
]
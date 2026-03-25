from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('register_user/',views.register_user,name="register_user"),

    # api
    path('get_sensor_data/',views.get_sensor_data,name="get_sensor_data"),
    path('get_rfid_api/',views.get_rfid_api,name="get_rfid_api"),
]
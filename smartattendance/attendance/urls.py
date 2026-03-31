from django.urls import path
from . import views
from attendance.views import home

urlpatterns = [
    path('', home, name='home'),

    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # Register user
    path('register_user/',views.register_user,name="register_user"),
    path('all_user/',views.all_user,name="all_user"),
    path('all_attendance/',views.all_attendance,name="all_attendance"),
    
    # get rfid api
    path('get-rfid/', views.get_rfid, name="get_rfid"),

    # Attendance creation API
    path('create_attendance/',views.create_attendance,name="create_attendance"),

    # api
    path('get-sensor/',views.get_sensor_data,name="get_sensor_data"),
    path('send-relay/',views.get_rfid_api,name="get_rfid_api"),
]
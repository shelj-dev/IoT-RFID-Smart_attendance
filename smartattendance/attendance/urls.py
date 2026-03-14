from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('attendance/', views.attendance_mark, name='attendance'),
    path('history/', views.history, name='history'),
    path('login/', views.student_login, name='login'),   # ✅ LOGIN
    path('logout/', views.student_logout, name='logout'),
    path('profile/', views.profile, name='profile'),
]
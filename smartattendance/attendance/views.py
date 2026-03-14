from django.shortcuts import render, redirect
from .models import Student, Attendance
from django.http import HttpResponse
from django.utils import timezone
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
def home(request):
    return render(request, 'home.html')


# def register(request):
#     if request.method == "POST":
#         username = request.POST['username']
#         password = request.POST['password']


#         user = authenticate(request, username=username, password=password)

#         if user is not None:
#             login(request, user)
#             return redirect('dashboard')
#         else:
#             messages.error(request, "Invalid Username or Password")

#         # return render(request, "login.html")
#         name = request.POST['name']
#         roll = request.POST['roll']
#         dept = request.POST['dept']
#         year = request.POST['year']
#         uid = request.POST['uid']

#         if User.objects.filter(username=username).exists():
#             messages.error(request, "Username already exists")
#             return redirect('register')

#         user = User.objects.create_user(
#             username=username,
#             password=password
#         )


#         if Student.objects.filter(rfid_uid=uid).exists():
#             return render(request, "register.html", {
#                 "error": "This RFID card is already registered!"
#             })


#         Student.objects.create(
#             user=user,
#             name=name,
#             roll_number=roll,
#             department=dept,
#             year=year,
#             rfid_uid=uid
#         )
#         messages.success(request, "Registration successful!")
#         return redirect('login')
#         # return redirect('home')
    
    

#     return render(request, 'register.html')
def register(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        name = request.POST.get('name')
        roll = request.POST.get('roll')
        dept = request.POST.get('dept')
        year = request.POST.get('year')
        uid = request.POST.get('uid')

        # 🔴 ADD THIS CHECK
        if not username or not password:
            messages.error(request, "Username and Password are required")
            return redirect('register')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect('register')

        if Student.objects.filter(rfid_uid=uid).exists():
            messages.error(request, "This RFID card is already registered!")
            return redirect('register')

        user = User.objects.create_user(
            username=username,
            password=password
        )

        Student.objects.create(
            user=user,
            name=name,
            roll_number=roll,
            department=dept,
            year=year,
            rfid_uid=uid
        )

        messages.success(request, "Registration successful!")
        return redirect('login')

    return render(request, 'register.html')



# def dashboard(request):
#     students = Student.objects.all()
#     return render(request, 'dashboard.html', {'students': students})
# def dashboard(request, student_id):
#     student = Student.objects.get(id=student_id)
#     records = Attendance.objects.filter(student=student).order_by('-date')[:5]

#     total_classes = Attendance.objects.filter(student=student).count()
#     present_count = total_classes

#     if total_classes > 0:
#         percentage = (present_count / total_classes) * 100
#     else:
#         percentage = 0

#     context = {
#         'student': student,
#         'records': records,
#         'total_classes': total_classes,
#         'present_count': present_count,
#         'percentage': round(percentage, 2)
#     }

#     return render(request, 'dashboard.html', context)
from django.contrib.auth.decorators import login_required

@login_required
def dashboard(request):
    student = Student.objects.get(user=request.user)

    records = Attendance.objects.filter(student=student).order_by('-date')[:5]
    total_classes = Attendance.objects.filter(student=student).count()
    present_count = total_classes

    percentage = (present_count / total_classes * 100) if total_classes > 0 else 0

    context = {
        'student': student,
        'records': records,
        'total_classes': total_classes,
        'present_count': present_count,
        'percentage': round(percentage, 2)
    }

    return render(request, 'dashboard.html', context)


@login_required
def profile(request):
    student = Student.objects.get(user=request.user)
    return render(request, "profile.html", {"student": student})

def attendance_mark(request):
    uid = request.GET.get('uid')

    try:
        student = Student.objects.get(rfid_uid=uid)
        Attendance.objects.create(student=student)
        return HttpResponse("Attendance Marked Successfully")
    except:
        return HttpResponse("Invalid Card")


def history(request):
    records = Attendance.objects.all()
    return render(request, 'history.html', {'records': records})

# def student_login(request):
#     if request.method == "POST":
#         username = request.POST['username']
#         password = request.POST['password']

#         user = authenticate(request, username=username, password=password)

#         if user is not None:
#             login(request, user)
#             return redirect('dashboard')
#         else:
#             messages.error(request, "Invalid Username or Password")

#     return render(request, 'login.html')
# def student_logout(request):
#         logout(request)
#         return render(request, 'logout.html')
#         # return redirect('login')
def student_login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, "Invalid Username or Password")

    return render(request, 'login.html')
def student_logout(request):
    logout(request)
    return redirect('login')

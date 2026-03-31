import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import SensorRFID, Attendance, Profile
from django.views.decorators.http import require_GET
from django.utils import timezone
from django.shortcuts import render, redirect, get_object_or_404
from .forms import *
from django.utils.timezone import now
from datetime import timedelta
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth import logout


def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("home")
        else:
            messages.error(request, "Invalid username or password")

    return render(request, "login.html")


def logout_view(request):
    logout(request)
    return redirect("login")


def home(request):
    return render(request, "home.html")


def create_attendance(rfid):
    user = Profile.objects.filter(rfid=rfid).first()

    if not user:
        print("not user")
        return "User does not exist"

    today_date = now().date()

    already_marked = Attendance.objects.filter(
        user=user,
        time_in__date=today_date
    ).exists()

    if already_marked:
        return "Already attendance registered"

    Attendance.objects.create(user=user)
    return "Attendance created"


def register_user(request):
    form = ProfileForm()
    if request.method == "POST":
        form = ProfileForm(request.POST)
        if form.is_valid():
            profile = form.save(commit=False)

            rfid = request.POST.get("rfid")

            if not rfid:
                form.add_error(None, "RFID is required. Please scan your card.")
                return render(request, "new/register_user.html", {"form": form})

            profile.rfid = rfid
            profile.save()

            return redirect("home")

    return render(request, "register_user.html", {"form": form})


@csrf_exempt
def get_rfid(request):
    rfid_obj = SensorRFID.objects.order_by("-time_stamp").first()

    if not rfid_obj:
        return JsonResponse({"rfid": None, "error": "No data available"})

    if now() - rfid_obj.time_stamp > timedelta(seconds=5):
        return JsonResponse({"rfid": None, "error": "Card not found"})

    if Profile.objects.filter(rfid=rfid_obj.rfid_data).exists():
        return JsonResponse({
            "rfid": None,
            "error": "This tag is already registered"
        })

    return JsonResponse({
        "rfid": rfid_obj.rfid_data
    })


# PICO API
@csrf_exempt
def get_sensor_data(request):

    if request.method != "POST":
        return JsonResponse({"error": "POST required"}, status=405)

    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        print("Error")
        return JsonResponse({"error": "Invalid JSON"}, status=400)

    print(data)
    value = data.get("rfid")


    if not value:
        attendance_message = None
    else:
        SensorRFID.objects.create(rfid_data=value)
        print("Sensor value:", value)
        attendance_message = create_attendance(value)
        print(attendance_message)
        # attendance_message = None

    return JsonResponse({
        "status": "received",
        "rfid": value,
        "attendance": attendance_message
    })


# PICO api
def get_rfid_api(request):
    rfid = SensorRFID.objects.order_by("-time_stamp").first()

    if not rfid:
        return JsonResponse({"message": "No data available"})

    if now() - rfid.time_stamp <= timedelta(seconds=5):
        return JsonResponse({"message": rfid.rfid_data})
    else:
        return JsonResponse({"message": "Card not found"})


def all_user(request):
    data = Profile.objects.all()
    return render(request, "all_user.html", {"data":data})


def all_attendance(request):
    attendance = Attendance.objects.all().order_by("-time_in")
    return render(request, "attendance.html", {"attendance":attendance})

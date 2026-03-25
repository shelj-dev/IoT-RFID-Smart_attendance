import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import SensorRFID, Attendance, Profile
from django.views.decorators.http import require_GET
from django.utils import timezone
from django.shortcuts import render, redirect
from .forms import *
from django.utils.timezone import now
from datetime import timedelta


def home(request):
    return render(request, "new/home.html")


def create_attendance(rfid):
    try:
        user = Profile.objects.get(rfid=rfid)
    except Profile.DoesNotExist:
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


@csrf_exempt
def get_sensor_data(request):

    if request.method != "POST":
        return JsonResponse({"error": "POST required"}, status=405)

    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON"}, status=400)

    value = data.get("rfid")

    if not value:
        return JsonResponse({"error": "RFID is required"}, status=400)

    last = SensorRFID.objects.order_by("-time_stamp").first()
    if last and last.rfid_data == value and now() - last.time_stamp < timedelta(seconds=2):
        return JsonResponse({"status": "duplicate ignored"})

    SensorRFID.objects.create(rfid_data=value)
    print("Sensor value:", value)

    attendance_message = create_attendance(value)

    return JsonResponse({
        "status": "received",
        "rfid": value,
        "attendance": attendance_message
    })


def register_user(request):
    form = ProfileForm()
    if request.method == "POST":
        form = ProfileForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("home")
    return render(request, "new/register_user.html", {"form":form})


def get_rfid_api(request):
    rfid = SensorRFID.objects.order_by("-time_stamp").first()

    if not rfid:
        return JsonResponse({"message": "No data available"})

    if now() - rfid.time_stamp <= timedelta(seconds=5):
        return JsonResponse({"message": rfid.rfid_data})
    else:
        return JsonResponse({"message": "Card not found"})



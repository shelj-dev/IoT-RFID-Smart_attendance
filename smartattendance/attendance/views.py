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
from django.http import JsonResponse
from django.utils import timezone
from datetime import timedelta



def home(request):
    return render(request, "new/home.html")


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

            rfid = request.POST.get("rfid")  # ✅ get from POST directly

            if not rfid:
                form.add_error(None, "RFID is required. Please scan your card.")
                return render(request, "new/register_user.html", {"form": form})

            profile.rfid = rfid
            profile.save()

            return redirect("home")

    return render(request, "new/register_user.html", {"form": form})


@csrf_exempt
def get_rfid(request):
    data = SensorRFID.objects.last()
    
    if data is None:
        return JsonResponse({"rfid": None})
    
    # Check if timestamp is within last few seconds
    if timezone.now() - data.time_stamp <= timedelta(seconds=5):
        rfid = data.rfid_data
    else:
        rfid = None

    print("RFID frontend:", rfid)

    return JsonResponse({"rfid": rfid})

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

import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import SensorRFID, Attendance, Profile
from django.views.decorators.http import require_GET
from django.utils import timezone


@csrf_exempt
def get_sensor_data(request):

    if request.method == "POST":
        data = json.loads(request.body)

        value = data.get("rfid")
        SensorRFID.objects.create(rfid_data=value)
        print("Sensor value:", value)

        return JsonResponse({
            "status": "received",
            "sensor": value
        })

    return JsonResponse({"error": "POST required"})


@require_GET
def send_sensor_data(request):

    data = {
        "relay": "hello"
    }

    latest_sensor = SensorRFID.objects.order_by('-id').first()

    if not latest_sensor or not latest_sensor.rfid_data:
        data.update({
            "status": "error",
            "message": "No RFID data"
        })
        return JsonResponse(data)

    rfid_value = latest_sensor.rfid_data

    
    user = Profile.objects.filter(rfid=rfid_value).first()

    if not user:
        data.update({
            "status": "invalid",
            "message": "RFID not registered",
            "rfid": rfid_value
        })
        return JsonResponse(data)

    
    today = timezone.now().date()
    attendance = Attendance.objects.filter(user=user, date=today).first()

    if attendance:
        if attendance.logout_time is None:
            attendance.logout_time = timezone.now()
            attendance.save()

            data.update({
                "status": "logout",
                "user": user.name
            })
        else:
            data.update({
                "status": "already_logged_out",
                "user": user.name
            })
    else:
        Attendance.objects.create(
            user=user,
            date=today,
            login_time=timezone.now()
        )

        data.update({
            "status": "login",
            "user": user.name
        })

    return JsonResponse(data)

    # check the RFID data with the available users.
    # if user exists check loggedin
    # if not loggedin register the user as loggedin 

    



# Register new user by admin
# Connect rfid to the user

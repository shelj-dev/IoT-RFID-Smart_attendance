import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import SensorRFID, Attendance, Profile
from django.views.decorators.http import require_GET


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

    # check the RFID data with the available users.
    # if user exists check loggedin
    # if not loggedin register the user as loggedin 

    return JsonResponse(data)



# Register new user by admin
# Connect rfid to the user

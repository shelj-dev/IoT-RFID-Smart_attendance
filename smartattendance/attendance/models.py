from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    username = models.CharField(max_length=150)
    roll_no = models.CharField(max_length=50)
    rfid = models.CharField(max_length=50)

    def __str__(self):
        return self.username


class Attendance(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    time_in = models.DateTimeField(auto_now=False, auto_now_add=True)

    class Meta:
        unique_together = ('user', 'time_in')

    def __str__(self):
        return f"{self.user.username} - {self.time_in}"


class SensorRFID(models.Model):
    rfid_data = models.CharField(max_length=150)
    time_stamp = models.DateTimeField(auto_now=False, auto_now_add=True)

    def __str__(self):
        return f"{self.time_stamp}"
    

from django.db import models

# Create your models here.

# class Student(models.Model):
#     name = models.CharField(max_length=100)
#     roll_number = models.CharField(max_length=20)
#     department = models.CharField(max_length=100)
#     year = models.IntegerField()
#     rfid_uid = models.CharField(max_length=50, unique=True)

#     def __str__(self):
#         return self.name
from django.db import models
from django.contrib.auth.models import User

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # ADD THIS
    name = models.CharField(max_length=100)
    roll_number = models.CharField(max_length=20)
    department = models.CharField(max_length=100)
    year = models.IntegerField()
    rfid_uid = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class Attendance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    time = models.TimeField(auto_now_add=True)
    status = models.CharField(max_length=10, default="Present")

    def __str__(self):
        return f"{self.student.name} - {self.date}"
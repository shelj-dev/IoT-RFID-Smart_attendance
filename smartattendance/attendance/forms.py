from django import forms
from attendance.models import Attendance, Profile


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ["rfid"]


class AttendanceForm(forms.ModelForm):
    class Meta:
        model = Attendance
        fields = "__all__"



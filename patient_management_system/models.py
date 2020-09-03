from django.db import models
from django.utils import timezone
import datetime
from django.contrib.auth.models import User

department = [('', 'Department'),
              ('General medicine', 'General medicine'),
              ('Urology', 'Urology'),
              ('Dermatology', 'Dermatology'),
              ('Neurology', 'Neurology'),
              ('Nephrology', 'Nephrology'),
              ('Dental', 'Dental')]


# Create your models here.
class doctors(models.Model):
    photo = models.FileField(default=None, upload_to='uploads/%Y-%m-%d/')
    name = models.CharField(max_length=30)
    dob = models.DateField()
    gender = models.CharField(choices=[('Male', 'Male'),
                                       ('Female', 'Female'), ], max_length=6)
    mobile = models.CharField(max_length=10)
    email = models.EmailField(default=None)
    address = models.TextField(max_length=300)
    qualification = models.CharField(max_length=75)
    experience = models.IntegerField(default=0)
    date_of_joining = models.DateField(default=datetime.datetime.now)
    department = models.CharField(choices=department, max_length=17)
    doctorate_copy = models.FileField(default=None, upload_to='uploads/%Y-%m-%d/')
    shift = models.CharField(choices=[('DAY', 'DAY'),
                                      ('NIGHT', 'NIGHT')], max_length=5)


class patients(models.Model):
    name = models.CharField(max_length=30)
    age = models.IntegerField(default=0)
    gender = models.CharField(choices=[('Male', 'Male'), ('Female', 'Female')], max_length=6)
    address = models.TextField(max_length=100)
    mobile = models.CharField(max_length=10)
    email = models.EmailField(default=None)
    datetime = models.DateTimeField(default=datetime.datetime.now)


class out_patient(models.Model):
    patient = models.ForeignKey(patients, on_delete=models.CASCADE, default=None)
    consultant_doctor = models.ForeignKey(doctors, on_delete=models.CASCADE, default=None)
    created = models.DateTimeField(auto_now=True)


class appointment(models.Model):
    patient = models.ForeignKey(patients, on_delete=models.CASCADE, default=None)
    consultant_doctor = models.ForeignKey(doctors, on_delete=models.CASCADE, default=None)
    created = models.DateTimeField()

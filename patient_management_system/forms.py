from django.contrib.admin import widgets
from PIL import Image
from .models import patients, department, doctors, out_patient, appointment
from django import forms
import datetime
from datetime import date
from django.core.exceptions import ValidationError
from .models import department
from django.contrib.auth.models import User


class DateInput(forms.DateInput):
    input_type = 'date'


class add_doctors_form(forms.ModelForm):
    photo = forms.FileField(label="profile picture", label_suffix='',
                            widget=forms.FileInput(attrs={'placeholder': 'photo', 'title': 'PROFILE'}))
    name = forms.CharField(label='Doctor Name', label_suffix='',
                           widget=forms.TextInput(attrs={'placeholder': 'Doctor Name'}))
    dob = forms.DateField(label="D.O.B", label_suffix='',
                          widget=DateInput(attrs={'placeholder': 'DOB', 'title': 'DATE OF BIRTH'}))
    gender = forms.ChoiceField(label="Gender", label_suffix='', choices=[('', 'GENDER'), ('Male', 'Male'),
                                                                         ('Female', 'Female'), ])
    mobile = forms.CharField(label='Mobile No', label_suffix='', max_length=10,
                             widget=forms.TextInput(attrs={'placeholder': 'Mobile No'}))
    email = forms.EmailField(label='Email  ', label_suffix='', widget=forms.EmailInput(attrs={'placeholder': 'Email'}))
    address = forms.CharField(label="Address", label_suffix='',
                              widget=forms.TextInput(attrs={'placeholder': 'Address'}))
    qualification = forms.CharField(label="Qualification", label_suffix='', max_length=75,
                                    widget=forms.TextInput(attrs={'placeholder': 'Qualification'}))
    experience = forms.IntegerField(label="Experience", label_suffix='',
                                    widget=forms.NumberInput(attrs={'placeholder': 'Experience'}))
    date_of_joining = forms.DateField(label="Date Of Joining", label_suffix='',
                                      widget=forms.DateInput(attrs={'readonly': True}),
                                      initial=datetime.date.today())
    department = forms.ChoiceField(label="Department", label_suffix='', choices=department)
    doctorate_copy = forms.FileField(label="Doctorate copy", label_suffix='', widget=forms.FileInput(
        attrs={'placeholder': 'doctorate_copy', 'title': 'DOCTORATE COPY'}))
    shift = forms.ChoiceField(label='Shift', label_suffix='', choices=[('', 'Shift'), ('DAY', 'DAY'),
                                                                       ('NIGHT', 'NIGHT')])

    class Meta:
        model = doctors
        fields = ['photo', 'name', 'dob', 'gender', 'mobile', 'email', 'address', 'qualification', 'experience',
                  'date_of_joining', 'department', 'shift', 'doctorate_copy', ]


class add_patients_form(forms.ModelForm):
    name = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder': 'Patient Name'}))
    age = forms.IntegerField(label='', widget=forms.NumberInput(attrs={'placeholder': 'Age'}))
    gender = forms.ChoiceField(label='', choices=[('', 'Gender'), ("Male", "Male"), ("Female", "Female")])
    address = forms.CharField(label='', max_length=200, widget=forms.TextInput(attrs={'placeholder': 'Address'}))
    mobile = forms.CharField(label='', max_length=10, widget=forms.TextInput(attrs={'placeholder': 'Mobile'}))
    email = forms.EmailField(label='', widget=forms.EmailInput(attrs={'placeholder': 'Email'}))
    datetime = forms.DateTimeField(label='',
                                   widget=forms.DateTimeInput(attrs={'readonly': True, 'hidden': True}),
                                   initial=datetime.date.today())

    class Meta:
        model = patients
        fields = ['name',
                  'age',
                  'gender',
                  'address',
                  'mobile',
                  'email',
                  'datetime'
                  ]

    def clean_name(self):
        return self.cleaned_data['name'].lower()


class out_patient_form(forms.ModelForm):
    name = forms.CharField(label='Patients Name', label_suffix='',
                           widget=forms.TextInput(
                               attrs={'placeholder': 'Patient name', 'class': 'form_input', 'readonly': True}))
    mobile = forms.CharField(label='Mobile No', label_suffix='',
                             widget=forms.TextInput(
                                 attrs={'placeholder': 'Mobile No', 'class': 'form_input', 'readonly': True}))
    consultant_doctor = forms.CharField(label='Consultant Doctor', label_suffix='',
                                        widget=forms.TextInput(
                                            attrs={'placeholder': 'Consultant_doctor', 'class': 'form_input'}))
    department = forms.ChoiceField(label='Department', label_suffix='', choices=department, )

    class Meta:
        model = out_patient
        fields = ['name',
                  'mobile',
                  'consultant_doctor',
                  'department',
                  ]


class appointment_form(forms.ModelForm):
    name = forms.CharField(label='Patients Name', label_suffix='',
                           widget=forms.TextInput(
                               attrs={'placeholder': 'Patient name', 'class': 'form_input', 'readonly': True}))
    mobile = forms.CharField(label='Mobile No', label_suffix='',
                             widget=forms.TextInput(
                                 attrs={'placeholder': 'Mobile No', 'class': 'form_input', 'readonly': True}))
    consultant_doctor = forms.CharField(label='Consultant Doctor', label_suffix='',
                                        widget=forms.TextInput(
                                            attrs={'placeholder': 'Consultant_doctor', 'class': 'form_input'}))
    department = forms.ChoiceField(label='Department', label_suffix='', choices=department, )

    class Meta:
        model = appointment
        fields = ['name',
                  'mobile',
                  'consultant_doctor',
                  'department',
                  'created'
                  ]

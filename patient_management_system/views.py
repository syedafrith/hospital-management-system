from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from .models import doctors, patients, out_patient, appointment
from django.http import JsonResponse, HttpResponse
import datetime
from django.db.models import Q
from .forms import add_patients_form, add_doctors_form, out_patient_form, appointment_form
from firstproject.settings import EMAIL_HOST_USER
from django.core.mail import send_mail


def appointment_reminder():
    for x in patients.objects.values_list('email'):
        subject = 'HOSPITAL_MANAGEMENT'
        message = 'MR/MRS ' + x.name + 'you name has been registered with our hospital.hope you will cure soon'
        email = list(x)
        try:
            send_mail(subject,
                      message, EMAIL_HOST_USER, email, fail_silently=False)
        except:
            print('not working')


def account_login(request):
    if request.method == "POST":
        name = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=name, password=password)
        if user is not None:
            login(request, user)
            return redirect('/patients')
        else:
            return HttpResponse("failed")
    return render(request, 'login.html')


@login_required(login_url='/login')
def doctors_data(request):
    doctors_form = add_doctors_form()
    doctors_list = doctors.objects.all()
    no_of_doctors = doctors.objects.all().count()
    return render(request, 'doctors_data.html',
                  {'doctors_list': doctors_list, 'doctors_form': doctors_form, 'no_of_doctors': no_of_doctors})


@login_required(login_url='/login')
def doctors_edit(request, my_id):
    obj = doctors.objects.get(id=my_id)
    if request.method == "POST":
        form3 = add_doctors_form(request.POST, request.FILES or None, instance=obj)
        if form3.is_valid():
            form3.save()
            messages.error(request, 'successfully updated')
    else:
        form3 = add_doctors_form(instance=obj)
        form3.fields['photo'].required = False
        form3.fields['doctorate_copy'].required = False
    return render(request, 'doctors_edit.html', {'form': form3})


def doctors_delete(request):
    doctor = doctors.objects.all()
    if request.is_ajax() and request.method == "POST":
        doc_id = request.POST['id']
        obj = doctors.objects.get(id=doc_id)
        obj.delete()
        html = render_to_string(
            template_name="doctors_list_results.html",
            context={"doctor_list": doctor}
        )
        return JsonResponse(data=html, safe=False)


def doctors_view(request):
    if request.is_ajax() and request.method == "POST":
        doc_id = request.POST['id']
        form = doctors.objects.get(id=doc_id)

        html = render_to_string(
            template_name="doctors_profile.html",
            context={"form": form}
        )
        return JsonResponse(data=html, safe=False)


def doctors_add(request):
    doctors_form = add_doctors_form(request.POST, request.FILES or None)
    if doctors_form.is_valid():
        doctors_form.save()
        doctor = doctors.objects.all()
        html = render_to_string(
            template_name="doctors_list_results.html",
            context={"doctor_list": doctor}
        )
        return JsonResponse(data=html, safe=False)


def check_doctors_data(request):
    if request.is_ajax() and request.method == "POST":
        name_or_department = request.POST['name']
        doctor = doctors.objects.all().filter(Q(name=name_or_department) | Q(department=name_or_department))
        html = render_to_string(
            template_name="doctors_search_results.html",
            context={"doctors": doctor}
        )
        return JsonResponse(data=html, safe=False)
    else:
        return HttpResponse("failed")


@login_required(login_url='/login')
def patients_data(request):
    if request.user.is_superuser:
        patients_form = add_patients_form()
        patients_list = patients.objects.all()
        out_patients_form = out_patient_form()
        doctor = doctors.objects.all()
        forms = {'patients_list': patients_list, 'patients_form': patients_form,
                 'out_patients_form': out_patients_form, 'doctors': doctor}
        return render(request, 'patients_data.html', forms)
    else:
        return redirect('/appointments')


def patients_add(request):
    patients_form = add_patients_form(request.POST or None)
    if patients_form.is_valid():
        username = patients_form.cleaned_data['name']
        email = patients_form.cleaned_data['email']
        password = patients_form.cleaned_data['mobile']
        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()
        data = patients_form.save(commit=False)
        data.user = User.objects.get(username=username)
        data.save()
        """subject = 'HOSPITAL_MANAGEMENT'
        message = 'MR/MRS ' + username + ' your name has been registered with our hospital.hope you will cure soon'
        send_mail(subject,
                  message, EMAIL_HOST_USER, [email], fail_silently=False)"""
        patient = patients.objects.all()
        html = render_to_string(
            template_name="patients_list_results.html",
            context={"patients_list": patient}
        )
        return JsonResponse(data=html, safe=False)


@login_required(login_url='/login')
def patient_profile(request, id):
    patient = patients.objects.get(id=id)
    return render(request, 'patient_profile.html', {'patient': patient})


def check_patients_data(request):
    if request.is_ajax() and request.method == "POST":
        mobile = request.POST['mobile']
        data = patients.objects.all().filter(Q(name__iexact=mobile) | Q(mobile__iexact=mobile))
        html = render_to_string(
            template_name='patients_search_results.html',
            context={'form': data}
        )
        return JsonResponse(data=html, safe=False)
    else:
        return HttpResponse('failed')


@login_required(login_url='/login')
def out_patients_add(request):
    name = request.POST['name']
    mobile = request.POST['mobile']
    doctor = request.POST['consultant_doctor'].split(",")
    consultant_doctor = doctor[0]
    department = doctor[1]
    if doctors.objects.filter(name=consultant_doctor).filter(department=department).exists():
        consultant_doctor_id = doctors.objects.filter(name=consultant_doctor).values('id')
        patient_id = patients.objects.filter(mobile=mobile).filter(name=name).values('id')
        data = out_patient(patient_id=patient_id, consultant_doctor_id=consultant_doctor_id)
        data.save()
        messages.success(request, 'successfully added')
        success = 'successfully added'
        return JsonResponse(data=success, safe=False)
    else:
        return HttpResponse('failed')


@login_required(login_url='/login')
def patient_visit_history(request, id):
    if request.user.is_superuser:
        visit_history = out_patient.objects.filter(patient_id=id)
    else:
        patient_id = patients.objects.get(name=request.user)
        visit_history = out_patient.objects.filter(patient_id=patient_id.id)
    return render(request, 'patients_visit_history.html', {'visit_history': visit_history})


@login_required(login_url='/login')
def make_appointment(request, id):
    doctors_name = doctors.objects.all()
    patient_data = patients.objects.get(Q(pk=id) | Q(name=request.user))
    form = appointment_form()
    if request.method == "POST":
        name = request.POST['name']
        mobile = request.POST['mobile']
        doctor = request.POST['consultant_doctor'].split(",")
        consultant_doctor = doctor[0]
        department = doctor[1]
        datetime = request.POST['date_time']
        if doctors.objects.filter(name=consultant_doctor).filter(department=department).exists():
            consultant_doctor_id = doctors.objects.filter(name=consultant_doctor).values('id')
            patient_id = patients.objects.filter(mobile=mobile).filter(name=name).values('id')
            data = appointment(patient_id=patient_id, consultant_doctor_id=consultant_doctor_id, created=datetime)
            data.save()
            return redirect('/patients/')
    return render(request, 'new_appointment.html',
                  {'appointment_form': form, 'patients_data': patient_data, 'doctors': doctors_name})


@login_required(login_url='/login')
def manage_appointments(request):
    if not request.user.is_superuser:
        patient = patients.objects.get(name=request.user)
        appointments = appointment.objects.all().filter(patient_id=patient.id)
    else:
        appointments = appointment.objects.all().filter(created__gte=datetime.datetime.now())
        print(appointments)
    return render(request, 'appointments.html', {'appointment': appointments})

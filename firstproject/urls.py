"""firstproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('hospital_management_system/', include('hospital_management_system.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from patient_management_system import views
from django.contrib.auth import views as auth_views


app_name = 'patient_management_system'
urlpatterns = [
              path('admin/', admin.site.urls),
              path('login/', views.account_login,name='login'),
              path('logout/',auth_views.LogoutView.as_view(next_page='/login'),name='logout'),
              path('password-change/',auth_views.PasswordChangeView.as_view(template_name='password_change.html',success_url='/doctors')),
              path('password-change-success',auth_views.PasswordChangeDoneView.as_view()),
              path('doctors/', views.doctors_data, name='doctors_data'),
              path('doctors/add_doctors/', views.doctors_add, name="doctors_add"),
              path('doctors/view/', views.doctors_view, name="view"),
              path('doctors/<int:my_id>/edit/', views.doctors_edit, name="edit"),
              path('doctors/delete/', views.doctors_delete, name="delete"),
              path('doctors/check_doctors_data/', views.check_doctors_data, name="check_doctors_data"),
              path('patients/', views.patients_data, name='patients_data'),
              path('patients/add_patients/', views.patients_add, name="patients_add"),
              path('patients/check_patients_data/', views.check_patients_data, name="check_patients_data"),
              path('patients/out_patients/', views.out_patients_add, name="out_patients_add"),
              path('patient_profile/<int:id>/',views.patient_profile,name='patient_profile'),
              path('patients_visit_history/<int:id>', views.patient_visit_history,
                   name="patient_visit_history"),
              path('make_appointment/<int:id>/',views.make_appointment,name='make_appointment'),
              path('appointments/',views.manage_appointments,name='appointments'),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

from django.shortcuts import render, redirect
from .models import Appointment
from ..first_app.models import User
import datetime
from django.contrib import messages
today = datetime.datetime.today()
# Create your views here.
def index(request):
    current_user = User.objects.get(id=request.session['user_id'])
    context = {
        'today': today,
        'appointments_today' : Appointment.objects.filter(dated=today, user=current_user).order_by('time'),
        'other_appointments' : Appointment.objects.filter(user=current_user).exclude(dated=today).order_by('dated'),
        'all_appointments' : Appointment.objects.all(),
    }
    return render(request, 'appointments/index.html', context)

def add(request):
    viewsResponse = Appointment.objects.add_appointment(request.POST, request.session['user_id'])
    if viewsResponse['isAppointment']:
        return redirect('/appointments')
    else:
        for error in viewsResponse['errors']:
            messages.error(request, error)
        return redirect('/appointments')

def edit(request, appointment_id):
    context = {
        'this_appointment' : Appointment.objects.get(id=appointment_id)
    }
    return render(request, 'appointments/edit.html', context)

def update(request, appointment_id):
    print today
    viewsResponse = Appointment.objects.edit_appointment(request.POST, request.session['user_id'], appointment_id)
    if viewsResponse['isUpdate']:
        return redirect('/appointments')
    else:
        for error in viewsResponse['errors']:
            messages.error(request, error)
        return redirect('/edit/{}'.format(appointment_id))

def delete(request, appointment_id):
    delete = Appointment.objects.filter(id = appointment_id).delete()
    return redirect('/appointments')

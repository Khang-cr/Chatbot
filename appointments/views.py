from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Counsellor, Appointment
from .forms import AppointmentForm

def counsellor_list(request):
    counsellors = Counsellor.objects.all()
    return render(request, 'appointments/counsellor_list.html', {'counsellors': counsellors})

@login_required
def book_appointment(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.user = request.user
            appointment.save()
            return redirect('my_appointments')
    else:
        form = AppointmentForm()
    return render(request, 'appointments/book_appointments.html', {'form': form})

@login_required
def my_appointments(request):
    appointments = Appointment.objects.filter(user=request.user)
    return render(request, 'appointments/my_appointments.html', {'appointments': appointments})
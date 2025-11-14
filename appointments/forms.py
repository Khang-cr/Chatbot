from django import forms
from .models import Appointment

class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['counsellor', 'date_time', 'notes']
        widgets = {
            'date_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }
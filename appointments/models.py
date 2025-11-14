from django.db import models
from django.contrib.auth.models import User

class Counsellor(models.Model):
    name = models.CharField(max_length=100)
    specialty = models.CharField(max_length=200)
    availability = models.TextField()  # Ví dụ: "Thứ 2-6, 9AM-5PM"

    def __str__(self):
        return self.name

class Appointment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    counsellor = models.ForeignKey(Counsellor, on_delete=models.CASCADE)
    date_time = models.DateTimeField()
    notes = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=[('pending', 'Pending'), ('confirmed', 'Confirmed'), ('cancelled', 'Cancelled')], default='pending')

    def __str__(self):
        return f"{self.user.username} with {self.counsellor.name} at {self.date_time}"
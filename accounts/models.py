from django.db import models
from django.contrib.auth.models import User
# Define model classes to pull out data from database a present to the user

# Create your models here.
class UserProfile(models.Model):
    USER_TYPE_CHOICES = [
        ('student', 'Student'),
        ('therapist', 'Therapist'),
    ]
    
    VERIFICATION_STATUS = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    # User type
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES, default='student')
    
    # Verification for therapist
    verification_status = models.CharField(max_length=10, choices=VERIFICATION_STATUS, default='pending', null=True, blank=True)
    verification_document = models.ImageField(upload_to='verification_docs/', null=True, blank=True)
    verified_at = models.DateTimeField(null=True, blank=True)
    
    # Student info
    age = models.IntegerField(null=True, blank=True)
    gender = models.CharField(max_length=10, choices=[
        ('male', 'Male'),
        ('female', 'Female'),
    ], null=True, blank=True)
    occupation = models.CharField(max_length=100, null=True, blank=True)
    university = models.CharField(max_length=200, null=True, blank=True)
    
    # Additional fields
    phone = models.CharField(max_length=15, null=True, blank=True)
    emergency_contact = models.CharField(max_length=15, null=True, blank=True)
    emergency_contact_name = models.CharField(max_length=100, null=True, blank=True)

    year_of_study = models.IntegerField(null=True, blank=True, choices=[
        (1, 'Year 1'),
        (2, "Year 2"),
        (3, 'Year 3'),
        (4, 'Year 4'),
        (5, 'Other'),
    ])

    student_id = models.CharField(max_length=50, null=True, blank=True)
    has_previous_counseling = models.BooleanField(default=False)
    is_currently_in_theraphy = models.BooleanField(default=False)
    notes = models.TextField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return f"Profile of {self.user.username} ({self.user_type})"

class CounselingSession(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    session_date = models.DateTimeField()
    counselor_name = models.CharField(max_length=100)
    
    session_type = models.CharField(max_length=20, choices=[
        ('individual', 'Individual'),
        ('group', 'Group'),
        ('online', 'Online'),
        ('phone', 'Phone'),
    ])
    
    duration_minutes = models.IntegerField()
    notes = models.TextField()
    
    # Follow-up
    next_session_date = models.DateTimeField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-session_date']
    
    def __str__(self):
        return f"{self.user.username} - {self.session_date.strftime('%Y-%m-%d')}"

class DASS21Result(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    test_date = models.DateTimeField(auto_now_add=True)
    
    # Store answer (JSON or each field)
    answers = models.JSONField()
    
    # Score
    depression_score = models.IntegerField()
    anxiety_score = models.IntegerField()
    stress_score = models.IntegerField()
    
    # levels
    depression_level = models.CharField(max_length=20)  # Normal, Mild, Moderate, Severe, Extremely Severe
    anxiety_level = models.CharField(max_length=20)
    stress_level = models.CharField(max_length=20)
    
    def __str__(self):
        return f"{self.user.username} - {self.test_date.strftime('%Y-%m-%d')}"
    
class MentalHealthResource(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    
    resource_type = models.CharField(max_length=20, choices=[
        ('article', 'Article'),
        ('video', 'Video'),
        ('audio', 'Audio/Meditation'),
        ('hotline', 'Hotline'),
        ('app', 'Mobile App'),
    ])
    
    url = models.URLField(null=True, blank=True)
    phone = models.CharField(max_length=15, null=True, blank=True)
    
    # Suitable for which state
    for_depression = models.BooleanField(default=False)
    for_anxiety = models.BooleanField(default=False)
    for_stress = models.BooleanField(default=False)
    
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title


class ProgressNote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    
    mood_rating = models.IntegerField(choices=[
        (1, 'Very Poor'),
        (2, 'Poor'),
        (3, 'Fair'),
        (4, 'Good'),
        (5, 'Very Good'),
    ])
    
    sleep_hours = models.DecimalField(max_digits=3, decimal_places=1, null=True, blank=True)
    exercise_done = models.BooleanField(default=False)
    
    notes = models.TextField(null=True, blank=True)
    
    class Meta:
        ordering = ['-date']    
    def __str__(self):
        return f"{self.user.username} - {self.date}"
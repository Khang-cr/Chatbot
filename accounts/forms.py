from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserProfile

class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)
    user_type = forms.ChoiceField(
        choices=UserProfile.USER_TYPE_CHOICES,
        widget=forms.RadioSelect,
        initial='student'
    )
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

class TherapistVerificationForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['verification_document']
        widgets = {
            'verification_document': forms.FileInput(attrs={'accept': 'image/*'})
        }
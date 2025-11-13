from django.urls import path
from .views import (
    SignUpView, 
    student_basic_info_view,
    therapist_basic_info_view,
    dass21_test_view,
    dass21_result_view,
    student_profile_view,
    therapist_profile_view,
    therapist_verification_view,
    verification_pending_view,
)

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('basic-info/', student_basic_info_view, name='student_basic_info'),
    path('dass21-test/', dass21_test_view, name='dass21_test'),
    path('dass21-result/', dass21_result_view, name='dass21_result'),
    path('profile/', student_profile_view, name='student_profile'),
    path('therapist-basic-info/', therapist_basic_info_view, name='therapist_basic_info'),
    path('therapist-verification/', therapist_verification_view, name='therapist_verification'),
    path('therapist-profile/', therapist_profile_view, name='therapist_profile'),
    path('verification-pending/', verification_pending_view, name='verification_pending'),
]

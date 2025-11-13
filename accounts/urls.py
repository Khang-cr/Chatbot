from django.urls import path
from .views import (
    SignUpView, 
    collect_basic_info_view,
    therapist_basic_info_view,
    dass21_test_view,
    dass21_result_view,
    profile_detail_view,
    therapist_verification_view,
    verification_pending_view,
)

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('basic-info/', collect_basic_info_view, name='collect_basic_info'),
    path('dass21-test/', dass21_test_view, name='dass21_test'),
    path('dass21-result/', dass21_result_view, name='dass21_result'),
    path('profile/', profile_detail_view, name='profile_detail'),
    path('therapist-basic-info/', therapist_basic_info_view, name='therapist_basic_info'),
    path('therapist-verification/', therapist_verification_view, name='therapist_verification'),
    path('verification-pending/', verification_pending_view, name='verification_pending'),
]
from django.urls import path
from . import views

urlpatterns = [
    path('counsellors/', views.counsellor_list, name='counsellor_list'),
    path('book/', views.book_appointment, name='book_appointments'),
    path('my/', views.my_appointments, name='my_appointments'),
]
# from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path('register/student/', RegisterStudentView.as_view(), name='register_student'),
    path('',LoginView.as_view(),name='login'),
    path('otp/<int:user_id>/', OTPView.as_view(), name='otp'),
    path('logout/',LogoutView.as_view(), name='logout'),  # Logout endpoint
]
# from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path('',LoginView.as_view(),name='login'),
    path('otp/<int:user_id>/', OTPView.as_view(), name='otp'),
    path('logout/', LogoutView.as_view(), name='logout'),  # Logout endpoint
    path('subjects/',SubjectListView.as_view(),name='subjects'),
    path('chapters/',ChapterListView.as_view(),name='chapters')
]
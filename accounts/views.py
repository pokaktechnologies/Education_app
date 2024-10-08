from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .models import User, OTP
from .serializers import *
from django.utils import timezone
import random
import string
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import logout
from .serializers import LoginSerializer  # Keep your existing imports and LoginView
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib import messages
from .models import OTP, User
from django.core.mail import send_mail
from django.utils import timezone
import secrets
import re
from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from .serializers import UserSerializer, StudentProfileSerializer

class RegisterStudentView(APIView):
    def post(self, request):
        user_serializer = UserSerializer(data=request.data)
        if user_serializer.is_valid():
            user = user_serializer.save()

            student_data = {
                'user': user.id,  # User is already created, assign the user instance
                'mobile_number': request.data.get('mobile_number'),
                'syllabus': request.data.get('syllabus'),
                'standard': request.data.get('standard'),
            }
            student_serializer = StudentProfileSerializer(data=student_data)
            if student_serializer.is_valid():
                student_serializer.save(user=user)
                return Response({'message': 'Student registered successfully'}, status=status.HTTP_201_CREATED)
            else:
                # If student profile creation fails, delete the created user
                user.delete()
                return Response(student_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def generate_email_otp(user):
    try:
        delete_old_otps(user)
        otp = ''.join([str(secrets.randbelow(10)) for _ in range(6)])
        otp_instance, created = OTP.objects.update_or_create(user=user, defaults={'otp': otp})
        
        # Send the OTP via email
        subject = 'Your OTP for Verification'
        message = f'Your OTP is: {otp}'
        from_email = 'aiswaryasurendran97@gmail.com'
        recipient_list = [user.email]
        send_mail(subject, message, from_email, recipient_list)
        
        return otp, None

    except Exception as e:
        print(f"Error generating OTP: {str(e)}")
        return None, str(e)




class LoginView(generics.GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = LoginSerializer  # Specify the serializer class

    def get_object(self, queryset=None):
        user_id = self.kwargs.get('user_id')
        if user_id:
            return get_object_or_404(User, id=user_id) 
        return super().get_object(queryset)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        username = serializer.validated_data['username']
        password = serializer.validated_data['password']
        
        user = authenticate(username=username, password=password)
        if user is not None:
            # Successful login response
            otp, error_message = generate_email_otp(user)
            if error_message:  # Handle the OTP generation error
                messages.error(request, f"Failed to send OTP: {error_message}")
                return redirect('login')
            return redirect('otp', user.id)  # Pass user_id here
           # return Response({"message": "Login successful.", "username": user.username}, status=status.HTTP_200_OK)
        return Response({"error": "Invalid credentials."}, status=status.HTTP_401_UNAUTHORIZED)


def delete_old_otps(user):
    most_recent_otp = OTP.objects.filter(user=user).order_by('-created_at').first()
    if most_recent_otp:
        OTP.objects.filter(user=user).exclude(id=most_recent_otp.id).delete()

def validate_otp(user, otp):
    try:
        otp_entry = OTP.objects.get(user=user, otp=otp)
    except OTP.DoesNotExist:
        return None, 'Invalid OTP'
    
    # Current time
    current_time = timezone.now()

    # Check if the OTP is older than 5 minutes
    otp_age_limit = current_time - timezone.timedelta(minutes=5)

    if otp_entry.created_at < otp_age_limit:
        otp_entry.delete()
        return None, 'OTP has expired'

    return otp_entry, None


class OTPView(generics.GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = OTPSerializer

    def post(self, request, *args, **kwargs):
        user_id = kwargs.get('user_id')  # Get user_id from kwargs
        user = get_object_or_404(User, id=user_id)

        # Check if the request is to verify OTP
        if 'otp' in request.data:
            serializer = OTPSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            if serializer.is_valid():
                otp = serializer.validated_data['otp']
                delete_old_otps(user)
                otp_entry, error_message = validate_otp(user, otp)
                if error_message:
                    messages.error(request, error_message)
                    return Response({"error": error_message}, status=400)
                user.is_email_verified = True
                user.save()
                otp_entry.delete()
                return Response({"message": "OTP verified successfully."})
            return Response(serializer.errors, status=400)
        
        # Check if the request is to resend OTP
        elif request.data.get('action') == 'resend':
            otp, error_message = generate_email_otp(user)  # Call your OTP generation function
            if error_message:
                messages.error(request, f"Failed to send OTP: {error_message}")
                return Response({"error": error_message}, status=400)

            OTP.objects.create(user=user, otp=otp, created_at=timezone.now())
            messages.success(request, 'A new OTP has been sent to your email.')
            return Response({"message": "A new OTP has been sent to your email."})

        return Response({"error": "Invalid request."}, status=400)

        

class LogoutView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]  # Ensure the user is authenticated

    def post(self, request, *args, **kwargs):
        logout(request)
        return Response({"message": "Logout successful."}, status=status.HTTP_200_OK)
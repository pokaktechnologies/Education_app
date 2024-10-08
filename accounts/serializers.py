from rest_framework import serializers
from .models import User,OTP,StudentProfile, Syllabus, Standard
import random


class OTPSerializer(serializers.Serializer):
    otp = serializers.IntegerField()
    def validate(self, value):
        return value

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)

    def validate(self, data):
        return data
    
class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'gender']

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user

class StudentProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentProfile
        fields = ['mobile_number', 'syllabus', 'standard']

    def create(self, validated_data):
        student_profile = StudentProfile(**validated_data)
        student_profile.save()
        return student_profile

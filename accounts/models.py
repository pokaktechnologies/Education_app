import random
import string
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser, Group, Permission


class User(AbstractUser):
    is_creator = models.BooleanField(default=False)
    is_student = models.BooleanField(default=False)
    is_email_verified = models.BooleanField(default=False)
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
    ]
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)

    # groups = models.ManyToManyField(Group, related_name='custom_user_set', blank=True)
    # user_permissions = models.ManyToManyField(Permission, related_name='custom_user_permissions_set', blank=True)

    def __str__(self):
        return self.username


class OTP(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    otp = models.CharField(max_length=6, blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)


    def __str__(self):
        return f'{self.otp} OTP for {self.user.username}'
    


class CreatorProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # Connects to User model
    profile_picture = models.ImageField(upload_to='creator_profile_pics/', null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    subject_specialization = models.CharField(max_length=100)
    experience = models.PositiveIntegerField(help_text="Years of teaching experience", null=True, blank=True)
    is_verified = models.BooleanField(default=False)
    joined_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username
    


class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    mobile_number = models.CharField(max_length=15)
    syllabus = models.ForeignKey('Syllabus', on_delete=models.CASCADE)
    standard = models.ForeignKey('Standard', on_delete=models.CASCADE)
    enrolled_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username
    



class Syllabus(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Standard(models.Model):
    name = models.CharField(max_length=50)
    syllabus = models.ForeignKey(Syllabus, on_delete=models.CASCADE)  # Each standard is associated with a syllabus

    def __str__(self):
        return f'{self.name} - {self.syllabus.name}'


class Subject(models.Model):
    name = models.CharField(max_length=100)
    standard = models.ForeignKey(Standard, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.name} - {self.standard.name} - {self.standard.syllabus.name}'


class Chapter(models.Model):
    name = models.CharField(max_length=100)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.name} - {self.subject.name}'


class Content(models.Model):
    creator = models.ForeignKey(CreatorProfile, on_delete=models.CASCADE)  # Linked to the teacher
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE)  # Linked to a specific chapter
    title = models.CharField(max_length=255)
    description = models.TextField()
    file = models.FileField(upload_to='content_files/')
    upload_date = models.DateTimeField(auto_now_add=True)
    is_published = models.BooleanField(default=False)

    def __str__(self):
        return self.title




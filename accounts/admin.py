from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(User)
admin.site.register(OTP)
admin.site.register(Syllabus)
admin.site.register(Standard)
admin.site.register(Subject)
admin.site.register(Chapter)
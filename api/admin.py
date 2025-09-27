from django.contrib import admin
from .models import User, Company, Profile, Skill, Job, Application

# Register your models here.

# the simple way to register models here
admin.site.register(User)
admin.site.register(Company)
admin.site.register(Profile)
admin.site.register(Skill)
admin.site.register(Job)
admin.site.register(Application)
from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
# Let's do some magic here

###
#01. authentication & core user models
###
class User(AbstractUser):
    """
    Custom user model inheriting form Django's AbstractUser .
    we add a 'role' to distinguish between job Seekers and Recruiters
    """
    class Role(models.TextChoices):
        JOB_SEEKER = 'job_seeker', 'Job Seeker '
        RECRUITER = 'recruiter', 'Recruiter'
    role = models.CharField(max_length=20, choices=Role.choices , default=Role.JOB_SEEKER)

    def __str__(self):
        return self.username

class Company(models.Model):
    """
    Contains information about the company a recruiter belongs to
    """
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="companies",
        limit_choices_to={'role': User.Role.RECRUITER}
    )
    name = models.CharField(max_length=255)
    descriptions = models.TextField(blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    logo_url = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Profile(models.Model):
    """
    Contains additional information for a job Seeker.
    A one to one rel ensure each user has only one profile.
    """
    user = models.OneToOneField(
        User,
        on_delete= models.CASCADE,
        primary_key=True,
        related_name='profile',
        limit_choices_to={'role':User.Role.JOB_SEEKER}

    )

    full_name= models.CharField(max_length=255, blank=True)
    headline= models.CharField(max_length=255, blank=True)
    summary = models.TextField(blank=True, null=True)
    resume_url = models.URLField(blank=True, null=True)
    ##The many to many filed for skills is defined below, after skill model is created .
    skills= models.ManyToManyField('Skill', blank=True, related_name= 'profiles')
    created_at= models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username

####
##
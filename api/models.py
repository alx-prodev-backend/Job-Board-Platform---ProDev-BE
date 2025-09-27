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
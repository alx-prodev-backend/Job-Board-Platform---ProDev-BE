from django.db import models
from django.contrib.auth.models import AbstractUser

###
# 1. AUTHENTICATION & CORE USER MODELS
###

class User(AbstractUser):
    """
    Custom User Model inheriting from Django's AbstractUser.
    We add a 'role' field and fix the related_name clash for groups and permissions.
    """
    class Role(models.TextChoices):
        JOB_SEEKER = 'job_seeker', 'Job Seeker'
        RECRUITER = 'recruiter', 'Recruiter'

    role = models.CharField(max_length=20, choices=Role.choices, default=Role.JOB_SEEKER)

    # FIX for migration clash: Add unique related_name to avoid conflicts
    # with the default auth.User model.
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='api_user_set',  # Unique related_name
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        related_query_name='user',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='api_user_permissions_set',  # Unique related_name
        blank=True,
        help_text='Specific permissions for this user.',
        related_query_name='user',
    )

    def __str__(self):
        return self.username

class Company(models.Model):
    """
    Contains information about the company a Recruiter belongs to.
    """
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='companies',
        limit_choices_to={'role': User.Role.RECRUITER}
    )
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    logo_url = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Profile(models.Model):
    """
    Contains additional information for a Job Seeker.
    A One-to-One relationship ensures each user has only one profile.
    """
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True,
        related_name='profile',
        limit_choices_to={'role': User.Role.JOB_SEEKER}
    )
    full_name = models.CharField(max_length=255, blank=True)
    headline = models.CharField(max_length=255, blank=True)
    summary = models.TextField(blank=True, null=True)
    resume_url = models.URLField(blank=True, null=True)
    skills = models.ManyToManyField('Skill', blank=True, related_name='profiles')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username


###
# 2. SUPPORTING MODELS
###

class Skill(models.Model):
    """
    Stores a skill, like 'Python', 'Django', 'SQL', etc.
    This ensures skills are standardized across the platform.
    """
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


###
# 3. CORE JOB BOARD MODELS
###

class Job(models.Model):
    """
    Represents a job posting on the platform.
    """
    class JobType(models.TextChoices):
        FULL_TIME = 'full-time', 'Full-time'
        PART_TIME = 'part-time', 'Part-time'
        CONTRACT = 'contract', 'Contract'
        INTERNSHIP = 'internship', 'Internship'

    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='jobs')
    posted_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='jobs_posted',
        limit_choices_to={'role': User.Role.RECRUITER}
    )
    title = models.CharField(max_length=255)
    description = models.TextField()
    location = models.CharField(max_length=255, blank=True)
    salary_min = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    salary_max = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    job_type = models.CharField(max_length=20, choices=JobType.choices, default=JobType.FULL_TIME)
    skills = models.ManyToManyField(Skill, blank=True, related_name='jobs')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class Application(models.Model):
    """
    Represents a job application submitted by a Job Seeker for a Job.
    """
    class ApplicationStatus(models.TextChoices):
        SUBMITTED = 'submitted', 'Submitted'
        VIEWED = 'viewed', 'Viewed'
        REJECTED = 'rejected', 'Rejected'
        ACCEPTED = 'accepted', 'Accepted'

    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='applications')
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='applications',
        limit_choices_to={'role': User.Role.JOB_SEEKER}
    )
    status = models.CharField(
        max_length=20,
        choices=ApplicationStatus.choices,
        default=ApplicationStatus.SUBMITTED
    )
    resume_url = models.URLField(blank=True, null=True)
    cover_letter = models.TextField(blank=True, null=True)
    applied_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # This constraint ensures a user can only apply to a specific job once.
        constraints = [
            models.UniqueConstraint(fields=['user', 'job'], name='unique_application')
        ]

    def __str__(self):
        return f'{self.user.username} applied for {self.job.title}'
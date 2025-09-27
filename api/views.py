from django.shortcuts import render
from rest_framework import generics, viewsets, permissions
from .models import User, Job
from .serializers import UserSerializer, RegisterSerializer, JobSerializer
from .permissions import IsRecruiterOrReadOnly

###
# 1. Authentication and User Management Views
###

class RegisterView(generics.CreateAPIView):
    """
    API endpoint for user registration.
    Accessible by anyone.
    """
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny] # Anyone can register

class ManageUserView(generics.RetrieveUpdateAPIView):
    """
    API endpoint for the logged-in user to retrieve and update their profile.
    """
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        # This view should return the current user, not look up by pk
        return self.request.user

###
# 2. Job Board Views
###

class JobViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions for Jobs.
    """
    queryset = Job.objects.all().order_by('-created_at')
    serializer_class = JobSerializer
    permission_classes = [IsRecruiterOrReadOnly] # Use our custom permission

    def perform_create(self, serializer):
        # Automatically associate the job with the recruiter's company
        # and the recruiter themselves when a new job is created.
        recruiter_user = self.request.user
        company = recruiter_user.companies.first() # Assumes one company per recruiter
        if company:
            serializer.save(posted_by=recruiter_user, company=company)
        else:
            # Handle case where recruiter might not have a company setup
            from rest_framework.exceptions import ValidationError
            raise ValidationError("Recruiter profile is not associated with a company.")


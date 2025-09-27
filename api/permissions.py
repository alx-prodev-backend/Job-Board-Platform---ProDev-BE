# In api/permissions.py

from rest_framework import permissions

class IsRecruiterOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow recruiters to create/edit jobs.
    Allows read-only access for all other users (including anonymous).
    """

    def has_permission(self, request, view):
        # Allow read-only methods (GET, HEAD, OPTIONS) for everyone.
        if request.method in permissions.SAFE_METHODS:
            return True

        # For write methods (POST, PUT, DELETE),
        # only allow if the user is authenticated and is a recruiter.
        return request.user.is_authenticated and request.user.role == 'recruiter'
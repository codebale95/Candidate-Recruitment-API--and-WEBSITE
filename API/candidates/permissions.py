from rest_framework import permissions

class IsRecruiterOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow recruiters to edit candidates.
    Candidates can only view their own data.
    """

    def has_permission(self, request, view):
        # Allow unauthenticated access to browsable API interface
        if not request.user.is_authenticated:
            # Allow GET requests for browsable API (list view)
            if request.method in permissions.SAFE_METHODS and view.action == 'list':
                return True
            return False
        return True

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any authenticated user
        if request.method in permissions.SAFE_METHODS:
            # Candidates can only see their own application
            if request.user.role == 'candidate':
                return obj.email == request.user.email
            return True

        # Write permissions are only allowed to recruiters
        return request.user.role == 'recruiter'

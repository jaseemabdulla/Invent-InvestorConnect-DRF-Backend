from rest_framework.permissions import BasePermission


class IsEntrepreneur(BasePermission):
    def has_permission(self, request, view):
        # Check if the user is authenticated
        if request.user.is_authenticated:
            # Check if the user has the role 'entrepreneur'
            return request.user.role == 'entrepreneur'
        return False
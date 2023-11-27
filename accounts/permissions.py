from rest_framework.permissions import BasePermission


class IsEntrepreneur(BasePermission):
    def has_permission(self, request, view):
        # Check if the user is authenticated
        if request.user.is_authenticated:
            # Check if the user has the role 'entrepreneur'
            return request.user.role == 'entrepreneur'
        return False
    
    
class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return request.user.role == 'admin'
        return False
    
    
class IsInvestor(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return request.user.role == 'investor'
        return False
              
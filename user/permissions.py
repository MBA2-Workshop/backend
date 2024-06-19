from rest_framework import permissions


class IsInstructor(permissions.BasePermission):
    """
    Custom permission to only allow instructors to access.
    CFA can also access.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role >= 2


class IsCfa(permissions.BasePermission):
    """
    Custom permission to only allow CFAs to access.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 3

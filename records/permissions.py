from rest_framework.permissions import BasePermission

class IsAdminOrFaculty(BasePermission):
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        return request.user.groups.filter(name__in=['Admin', 'Faculty']).exists()

class IsOwnerOrStaff(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.groups.filter(name__in=['Admin', 'Faculty']).exists():
            return True
        return obj.owner == request.user
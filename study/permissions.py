from rest_framework.permissions import BasePermission


class IsModerator(BasePermission):
    def has_permission(self, request, view):
        if request.user.groups.filter(name='moderators').exists():
            return True
        return False


class IsOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        if obj.owner == request.user:
            return True
        return False

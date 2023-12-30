from rest_framework.permissions import BasePermission


class IsModerator(BasePermission):
    """Является ли пользователь модератором"""
    def has_permission(self, request, view):
        return request.user.groups.filter(name='moderators').exists()


class IsOwner(BasePermission):
    """Является ли пользователь владельцем"""
    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user

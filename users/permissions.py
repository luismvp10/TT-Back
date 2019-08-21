from rest_framework.permissions import BasePermission


class IsAllowedToWrite(BasePermission):

    def has_permission(self, request, view):
        return request.user.user_type == "administrator"
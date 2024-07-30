from rest_framework.permissions import BasePermission
from user.constants import UserPermissionEnum




class SuperPermission(BasePermission):
    def has_permission(self, request, view):
        return permission_checking(
            user_permissions=request.user.role.permissions.all(),
            permission_to_check=UserPermissionEnum.SUPER.value
        )

class AccountManagementPermission(BasePermission):
    def has_permission(self, request, view):
        return permission_checking(
            user_permissions=request.user.role.permissions.all(),
            permission_to_check=UserPermissionEnum.ACCOUNTMANAGEMENT.value
        )

class Permission1Permission(BasePermission):
    def has_permission(self, request, view):
        return permission_checking(
            user_permissions=request.user.role.permissions.all(),
            permission_to_check=UserPermissionEnum.PERMISSION1.value
        )

class Permission2Permission(BasePermission):
    def has_permission(self, request, view):
        return permission_checking(
            user_permissions=request.user.role.permissions.all(),
            permission_to_check=UserPermissionEnum.PERMISSION2.value
        )



def permission_checking(user_permissions, permission_to_check):
    for permission in user_permissions:
        if permission.codename == permission_to_check: return True
    return False
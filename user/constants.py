from enum import Enum


class UserPermissionEnum(Enum):
    SUPER = "SUPER"
    ACCOUNTMANAGEMENT = "ACCOUNTMANAGEMENT"
    PERMISSION1 = "PERMISSION1"
    PERMISSION2 = "PERMISSION2"


class AdminRoleEnum(Enum):
    SUPERADMIN = "Super Admin"
    ADMIN = "Admin"
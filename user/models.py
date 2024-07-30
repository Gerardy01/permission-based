from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, Group
import uuid



USER_PERMISSION = (
    ('SUPERADMIN', 'SUPERADMIN'),
    ('ADMIN', 'ADMIN'),
    ('PERMISSION1', 'PERMISSION1'),
    ('PERMISSION2', 'PERMISSION2'),
)


# accoaunt manager
class MyAccountManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, username, role, name, password):

        user = self.model(
            username=username,
            name=name,
            role_id= role.pk,
            password=password,
        )

        user.set_password(password)
        user.save(using=self._db)
        
        return user

    def create_superuser(self, username, name, password):
        
        superadmin, _ = Roles.objects.get_or_create(name='Super Admin')
        admin, _ = Roles.objects.get_or_create(name='Admin')

        permissions = UserPermission.objects.all()
        superadmin.permissions.set(permissions)
        admin.permissions.set(permissions.exclude(codename = 'SUPER'))

        user = self.model(
            username=username,
            name=name,
            role_id=superadmin.pk,
            password=password,
        )

        user.is_staff = True
        user.is_superuser = True

        user.set_password(password)
        user.save(using=self._db)
        
        return user



class UserPermission(models.Model):
    codename = models.CharField(max_length=50, unique=True, choices=USER_PERMISSION)
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.codename
    
class Roles(models.Model):
    role_id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=100, unique=True)
    permissions = models.ManyToManyField(
        UserPermission,
        verbose_name=("Permissions"),
        blank=True,
    )

    def __str__(self):
        return self.name
    
    def get_permissions(self):
        if self.permissions:
            return self.permissions.all()
        else:
            return []


class Account(AbstractBaseUser):
    account_id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True
    )
    username = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    role = models.ForeignKey(Roles, on_delete=models.CASCADE, verbose_name=('Role'), blank=True, null=True)

    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    is_archive = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['name']

    objects = MyAccountManager()


    def __str__(self):
        return self.username
    
    def get_user_permissions(self):
        if self.role:
            return self.role.permissions.all()
        else:
            return []
from rest_framework.response import Response
from rest_framework import viewsets, status
from rest_framework.decorators import action

from rest_framework.permissions import IsAuthenticated

from .models import Account, Roles, UserPermission
from .serializers import AccountSerializer, CreateAccountSerializer, CreateRoleSerializer, EditOwnAccount, RoleSerializer

from . import permissions, exceptions

# constants
from .constants import AdminRoleEnum, UserPermissionEnum



class AccountViewSet(viewsets.ViewSet):
    # make sure its authenticated, and only account with user management permission able to access this viewset
    permission_classes=[IsAuthenticated, permissions.AccountManagementPermission]

    def get_queryset(self):
        qs = Account.objects.all()
        return qs

    def list(self, request):

        try:
            qs = self.get_queryset()
            user = request.user

            # only super admin and admin that able to see admin
            if user.role.name not in [AdminRoleEnum.ADMIN.value, AdminRoleEnum.SUPERADMIN.value]:
                qs = qs.exclude(role__name__in = [AdminRoleEnum.SUPERADMIN.value, AdminRoleEnum.ADMIN.value])
            
            # make sure only super admin able to see super admin account
            if user.role.name != AdminRoleEnum.SUPERADMIN.value:
                qs = qs.exclude(role__name = AdminRoleEnum.SUPERADMIN.value)

            if qs.count() == 0:
                return Response({
                    "status" : "success",
                    "message" : "no data"
                }, status=status.HTTP_204_NO_CONTENT)

            serializer = AccountSerializer(qs, many = True)
            return Response({
                "status" : "success",
                "data" : serializer.data
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response(
                {"status": "failed", "message": "server error", "error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
    
    def create(self, request):
        serializer = CreateAccountSerializer(data=request.data)

        try:
            if not serializer.is_valid():
                return Response({
                    "status" : "failed",
                    "message" : "bad request",
                    "data" : serializer.errors
                }, status=status.HTTP_400_BAD_REQUEST)
            
            validated_data = serializer.validated_data

            user = request.user
            qs = self.get_queryset()

            # check if role exist
            try:
                registered_role = Roles.objects.get(role_id = validated_data['role_id'])
            except:
                return Response({
                    "status" : "failed",
                    "message" : "role does not exist",
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # check if user superadmin or admin
            is_superadmin = False
            is_admin = False
            if user.role.name == AdminRoleEnum.SUPERADMIN.value:
                is_superadmin = True
                is_admin = True
            if user.role.name == AdminRoleEnum.ADMIN.value:
                is_admin = True
            
            # check if user allowed to create specific role
            if registered_role.name == AdminRoleEnum.SUPERADMIN.value and not is_superadmin:
                raise exceptions.NoPermission('Only Super Admin can create another Super Admin')
            if registered_role.name == AdminRoleEnum.ADMIN.value and not is_admin:
                raise exceptions.NoPermission('Must at least Admin role that able to create new Admin')
            
            # check if username already used
            exist_user = qs.filter(username = validated_data['username'])
            if exist_user.exists():
                return Response({
                    "status" : "failed",
                    "message" : "username already exist"
                }, status=status.HTTP_409_CONFLICT)
            

            new_account = Account.objects.create_user(
                username = validated_data['username'],
                name = validated_data['name'],
                role = registered_role,
                password = validated_data['password']
            )

            return_serializer = AccountSerializer(new_account)

            return Response({
                "status" : "success",
                "data" : return_serializer.data
            }, status=status.HTTP_201_CREATED)

        except exceptions.NoPermission as e:
            return Response({
                "status" : 'failed',
                "message" : str(e)
            }, status=status.HTTP_403_FORBIDDEN)

        except Exception as e:
            return Response(
                {"status": "failed", "message": "server error", "error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
    
    # get user's own account info
    @action(
        methods=['GET'],
        detail=False,
        url_path='get-info',
        url_name='get-info',
        # since this method should be able to get account info without admin permission
        # we set new permission classes that only applied to this method
        # still need to be authenticated (IsAuthenticated), but no admin permission required
        permission_classes=[IsAuthenticated]
    )
    def get_account_info(self, request):
        try:
            qs = self.get_queryset()
            qs = qs.filter(account_id = request.user.account_id)

            if qs.count() == 0:
                return Response({
                    "status" : "success",
                    "message" : "no data"
                }, status=status.HTTP_204_NO_CONTENT)

            serializer = AccountSerializer(qs.first())
            return Response({
                "status" : "success",
                "data" : serializer.data
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response(
                {"status": "failed", "message": "server error", "error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
    
    # edit user's own account
    @action(
        methods=['PUT'],
        detail=False,
        url_path='edit',
        url_name='edit',
        # since this method should be able to edit without admin permission
        # we set new permission classes that only applied to this method
        # still need to be authenticated (IsAuthenticated), but no admin permission required
        permission_classes=[IsAuthenticated]
    )
    def edit_account(self, request):
        serializer = EditOwnAccount(data=request.data)
        try:
            if not serializer.is_valid():
                return Response({
                    "status" : "failed",
                    "message" : "bad request",
                    "data" : serializer.errors
                }, status=status.HTTP_400_BAD_REQUEST)
            
            validated_data = serializer.validated_data
            user = request.user
            qs = self.get_queryset()

            try:
                account = Account.objects.get(account_id = user.account_id)
            except:
                raise exceptions.NotFound('Account not found')
            
            exist_user = qs.filter(
                username = validated_data['new_username'],
            ).exclude(account_id = account.pk)

            if exist_user.exists():
                return Response({
                    "status" : "failed",
                    "message" : "username already exist"
                }, status=status.HTTP_409_CONFLICT)
            
            account.username = validated_data['new_username']
            account.save()

            serializer = AccountSerializer(account)
            return Response({
                "status" : "success",
                "message" : "account edited",
                "data" : serializer.data
            }, status=status.HTTP_200_OK)
        
        except exceptions.NotFound as e:
            return Response({
                "status": "failed",
                "message": str(e)
            }, status=status.HTTP_404_NOT_FOUND)
            
        except Exception as e:
            return Response(
                {"status": "failed", "message": "server error", "error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
    
    # change user own password
    @action(
        methods=['PUT'],
        detail=False,
        url_path='change-password',
        url_name='change-password',
        # since this method should be able to edit without admin permission
        # we set new permission classes that only applied to this method
        # still need to be authenticated (IsAuthenticated), but no admin permission required
        permission_classes=[IsAuthenticated]
    )
    def change_password(self, request):
        # change user own password here
        pass
    
    # archive account (no need to put permission_classes. since we want to use from class permission_classes)
    @action(
        methods=['PUT'],
        detail=False,
        url_path='archive',
        url_name='archive',
    )
    def archive_account(self, request):
        # archive account here
        pass

    


class RoleViewSet(viewsets.ViewSet):
    # only if authenticated, and have SUPER permission
    permission_classes=[IsAuthenticated, permissions.SuperPermission]


    def get_queryset(self):
        qs = Roles.objects.all()
        return qs
    

    def list(self, request):
        
        try:

            qs = self.get_queryset()
            user = request.user

            if user.role.name != AdminRoleEnum.SUPERADMIN.value:
                qs.exclude(name=AdminRoleEnum.SUPERADMIN.value)

            if qs.count() == 0:
                return Response({
                    "status" : "success",
                    "message" : "no data"
                }, status=status.HTTP_204_NO_CONTENT)
            
            return_serializer = RoleSerializer(qs, many=True)
            return Response({
                "status" : "success",
                "data" : return_serializer.data
            }, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response(
                {"status": "failed", "message": "server error", "error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
    

    def create(self, request):
        serializer = CreateRoleSerializer(data=request.data)
        try:
            if not serializer.is_valid():
                return Response({
                    "status" : "failed",
                    "message" : "bad request",
                    "data" : serializer.errors
                }, status=status.HTTP_400_BAD_REQUEST)
            
            validated_data = serializer.validated_data
            qs = self.get_queryset()

            # check if role name already exist
            exist_role = qs.filter(name = validated_data['name'])
            if exist_role.exists():
                return Response({
                    "status" : "failed",
                    "message" : "role already exist"
                }, status=status.HTTP_409_CONFLICT)
            
            # check if permission exist and not empty
            permission_code_names = validated_data['permission_code_names']
            permission_list = UserPermission.objects.filter(codename__in=permission_code_names)
            if permission_list.count() == 0:
                return Response({
                    "status" : "failed",
                    "message" : "No permission found"
                }, status= status.HTTP_400_BAD_REQUEST)
            
            # only Super Admin can have SUPER permission
            super_permission_exist = permission_list.filter(
                codename = UserPermissionEnum.SUPER.value
            ).exists()
            if super_permission_exist:
                raise exceptions.NoPermission('SUPER only can be assigned to Super Admin')

            # create role
            new_role = Roles.objects.create(
                name = validated_data['name']
            )
            new_role.permissions.set(permission_list)
            new_role.save()

            return_serializer = RoleSerializer(new_role)
            return Response({
                "status" : "success",
                "message" : "role created",
                "data" : return_serializer.data
            }, status=status.HTTP_201_CREATED)

        except exceptions.NoPermission as e:
            return Response({
                "status": "failed",
                "message": str(e)
            }, status=status.HTTP_403_FORBIDDEN)

        except Exception as e:
            return Response(
                {"status": "failed", "message": "server error", "error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
    

    def edit(self,request):
        # edit role here
        # prevent to edit "Super Admin" and "Admin"
        pass

    def remove(self, request):
        # delete role here if there is no account associated with it
        # prevent to delete "Super Admin" and "Admin"
        pass

from rest_framework import serializers
from .models import Account, Roles, UserPermission


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        exclude = ['password']


class CreateAccountSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
    name = serializers.CharField()
    role_id = serializers.IntegerField()

class EditOwnAccount(serializers.Serializer):
    new_username = serializers.CharField()


class UserPermissonSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserPermission
        fields = '__all__'


class RoleSerializer(serializers.ModelSerializer):
    permissions = UserPermissonSerializer(many=True)
    class Meta:
        model = Roles
        fields = '__all__'


class CreateRoleSerializer(serializers.Serializer):
    name = serializers.CharField()
    permission_code_names = serializers.ListField(
        child=serializers.CharField()
    )
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from user.models import Roles




class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):

        user.id = user.account_id

        token = super().get_token(user)

        token['account_id'] = str(user.account_id)
        token['username'] = user.username
        token['role'] = user.role.name
        token['permissions'] = [permission.codename for permission in user.get_user_permissions()]

        return token
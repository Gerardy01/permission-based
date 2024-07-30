from rest_framework.response import Response
from rest_framework import viewsets, status
from rest_framework.decorators import action

from rest_framework_simplejwt.views import TokenObtainPairView

# Serializers
from .serializers import MyTokenObtainPairSerializer



class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class Authentication(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.user
        token = serializer.validated_data

        data = {
            'test': 'another data'
        }

        """
            put token under httponly cookie
        """

        return Response({
            'status': 'success',
            'msg': 'success',
            'data': data,
            'refresh': token['refresh'],
            'access': token['access'],
        }, status=status.HTTP_200_OK)




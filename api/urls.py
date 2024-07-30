from django.urls import path, include
from . import views

from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView

# views
from .views import MyTokenObtainPairView, Authentication



urlpatterns = [
    path('get-token/', MyTokenObtainPairView.as_view(), name='get-token'),
    path('refresh-token/', TokenRefreshView.as_view(), name='refresh-token'),
    path('login/', Authentication.as_view(), name='login'),

    # other app routes
    path('user/', include('user.urls')),
]



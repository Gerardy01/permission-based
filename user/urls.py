from django.urls import path
from . import views

from rest_framework.routers import DefaultRouter

# Route
from .views import AccountViewSet, RoleViewSet

router = DefaultRouter()
router.register('', AccountViewSet, basename='account')
router.register('role', RoleViewSet, basename='role')

urlpatterns = router.urls
    

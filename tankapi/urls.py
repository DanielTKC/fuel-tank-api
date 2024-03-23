# urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TankViewSet, TankVolumeViewSet

router = DefaultRouter()
router.register(r'tanks', TankViewSet, basename='tank')
router.register(r'tank-volumes', TankVolumeViewSet, basename='tank-volume')

urlpatterns = [
    path('', include(router.urls)),
]
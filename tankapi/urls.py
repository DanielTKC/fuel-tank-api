# urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TankViewSet, TankVolumeViewSet, RunningAverageSalesView, DailyTanksViewSet, TankVolumeLookup

router = DefaultRouter()
router.register(r'tanks', TankViewSet, basename='tank')
router.register(r'tank-volumes', TankVolumeViewSet, basename='tank-volume')
router.register(r'daily-tank', DailyTanksViewSet, basename='daily-tank')

urlpatterns = [
    path('', include(router.urls)),
    path('tanks/<int:tank_id>/average-sales/<str:date>/', RunningAverageSalesView.as_view(),
         name='running-average-sales'),
    path('tank-volume-lookup/', TankVolumeLookup.as_view(), name='tank-volume-lookup'),

]
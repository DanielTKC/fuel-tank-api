from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from ..models import Tank, TankVolume, DailyTankSales
from ..views import TankVolumeViewSet


class RunningAverageSalesViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.tank = Tank.objects.create(name='Tank3')
        self.view = TankVolumeViewSet()

        # Create tank volume records
        volume1 = TankVolume.objects.create(tank_id=self.tank, volume=10, created_at='2023-01-01T10:00:00Z')
        volume2 = TankVolume.objects.create(tank_id=self.tank, volume=30, created_at='2023-01-01T11:00:00Z')
        volume3 = TankVolume.objects.create(tank_id=self.tank, volume=45, created_at='2023-01-08T09:00:00Z')
        volume4 = TankVolume.objects.create(tank_id=self.tank, volume=20, created_at='2023-01-08T13:00:00Z')
        volume5 = TankVolume.objects.create(tank_id=self.tank, volume=30, created_at='2023-01-14T23:00:00Z')
        volume6 = TankVolume.objects.create(tank_id=self.tank, volume=60, created_at='2023-01-15T14:00:00Z')
        volume7 = TankVolume.objects.create(tank_id=self.tank, volume=25, created_at='2023-01-22T10:00:00Z')
        volume8 = TankVolume.objects.create(tank_id=self.tank, volume=50, created_at='2023-01-22T15:00:00Z')
        volume9 = TankVolume.objects.create(tank_id=self.tank, volume=70, created_at='2023-01-22T20:00:00Z')
        volume10 = TankVolume.objects.create(tank_id=self.tank, volume=12, created_at='2023-01-29T10:30:00Z')
        volume11 = TankVolume.objects.create(tank_id=self.tank, volume=49, created_at='2023-01-29T12:30:00Z')

        self.view.create_daily_tank_sales(volume1)
        self.view.create_daily_tank_sales(volume2)
        self.view.create_daily_tank_sales(volume3)
        self.view.create_daily_tank_sales(volume4)
        self.view.create_daily_tank_sales(volume5)
        self.view.create_daily_tank_sales(volume6)
        self.view.create_daily_tank_sales(volume7)
        self.view.create_daily_tank_sales(volume8)
        self.view.create_daily_tank_sales(volume9)
        self.view.create_daily_tank_sales(volume10)
        self.view.create_daily_tank_sales(volume11)

    def test_running_average_sales(self):
        print("DailyTankSales Objects:", DailyTankSales.objects.all())
        url = reverse('running-average-sales', args=[self.tank.id, '2023-01-29'])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['average_sales'], 22)

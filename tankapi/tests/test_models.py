from datetime import timedelta

from django.test import TestCase
from django.utils import timezone
from ..models import Tank, TankVolume, DailyTankSales
from tankapi.views import TankVolumeViewSet


class DailyTankSalesModelTest(TestCase):
    def test_daily_tank_sales_creation(self):
        tank = Tank.objects.create(name='Tank2')

        created_at = timezone.now()
        volume1 = TankVolume.objects.create(tank_id=tank, volume=10, created_at=created_at)
        volume2 = TankVolume.objects.create(tank_id=tank, volume=30, created_at=created_at + timedelta(minutes=1))

        # Manually trigger the update_daily_tank_sales method
        view = TankVolumeViewSet()
        view.update_daily_tank_sales(volume1)
        view.update_daily_tank_sales(volume2)

        # Print out debugging information
        print("Tank ID:", tank.id)
        print("Created At:", created_at.date())
        print("TankVolume Objects:", TankVolume.objects.filter(tank_id=tank))
        print("DailyTankSales Objects:", DailyTankSales.objects.all())

        # Get the daily tank sales record
        daily_sales = DailyTankSales.objects.get(tank_id=tank, date=created_at.date())

        # Assert the sales value
        self.assertEqual(daily_sales.sales, 20)

from datetime import timezone, datetime

from django.db import models


class Tank(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20)


class TankVolume(models.Model):
    id = models.AutoField(primary_key=True)
    tank_id = models.ForeignKey(Tank, on_delete=models.CASCADE)
    volume = models.FloatField()
    created_at = models.DateTimeField(default=datetime.now)


class DailyTankSales(models.Model):
    id = models.AutoField(primary_key=True)
    tank_id = models.ForeignKey(Tank, on_delete=models.CASCADE)
    date = models.DateField()
    sales = models.FloatField(default=0)




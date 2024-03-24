from django.contrib import admin

# Register your models here.
from .models import DailyTankSales, TankVolume, Tank

admin.site.register(DailyTankSales)
admin.site.register(Tank)
admin.site.register(TankVolume)

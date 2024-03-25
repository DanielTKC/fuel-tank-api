from django.contrib import admin
from tankapi.models import Tank, TankVolume, DailyTankSales
# Register your models here.

admin.site.register(Tank)
admin.site.register(TankVolume)
admin.site.register(DailyTankSales)
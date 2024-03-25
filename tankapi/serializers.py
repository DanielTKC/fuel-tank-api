from rest_framework import serializers

from .models import Tank, TankVolume, DailyTankSales


class TankSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Tank
        fields = ['id', 'name']


class TankVolumeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = TankVolume
        fields = ['id', 'tank_id', 'volume', 'created_at']


class DailyTankSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = DailyTankSales
        fields = ['id', 'tank_id', 'date', 'sales']

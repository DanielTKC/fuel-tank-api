from datetime import datetime, timedelta
from django.db.models import Sum
from django.shortcuts import get_object_or_404
from django.utils.dateparse import parse_date, parse_datetime
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Tank, TankVolume, DailyTankSales
from .serializers import TankSerializer, TankVolumeSerializer, DailyTankSerializer
import logging

logger = logging.getLogger(__name__)


class TankViewSet(viewsets.ModelViewSet):
    queryset = Tank.objects.all()
    serializer_class = TankSerializer


class TankVolumeViewSet(viewsets.ModelViewSet):
    queryset = TankVolume.objects.all()
    serializer_class = TankVolumeSerializer

    def perform_create(self, serializer):
        tank_volume = serializer.save()
        self.create_daily_tank_sales(tank_volume)

    def perform_update(self, serializer):
        tank_volume = serializer.save()
        self.update_tank_volume_and_daily_sales(tank_volume)

    def calculate_sales(self, tank_volume, previous_volume=None, previous_day_last_volume=None):
        if previous_volume:
            sales = tank_volume.volume - previous_volume.volume
        elif previous_day_last_volume:
            sales = tank_volume.volume - previous_day_last_volume.volume
        else:
            sales = 0
        return sales

    def update_tank_volume_and_daily_sales(self, tank_volume):
        tank_id = tank_volume.tank_id
        created_at_date = tank_volume.created_at.date()

        # Delete all DailyTankSales records for the same tank and date
        DailyTankSales.objects.filter(tank_id=tank_id, date=created_at_date).delete()

        # Get all TankVolume records for the same tank and date
        tank_volumes = TankVolume.objects.filter(tank_id=tank_id, created_at__date=created_at_date).order_by('created_at')

        # Recalculate DailyTankSales for each TankVolume record
        for i, current_volume in enumerate(tank_volumes):
            if i == 0:
                previous_day_last_volume = TankVolume.objects.filter(
                    tank_id=tank_id,
                    created_at__date=created_at_date - timedelta(days=1)
                ).order_by('-created_at').first()

                if previous_day_last_volume:
                    sales = self.calculate_sales(current_volume, previous_day_last_volume=previous_day_last_volume)
                    DailyTankSales.objects.create(tank_id=tank_id, date=created_at_date, sales=max(sales, 0))
            else:
                previous_volume = tank_volumes[i - 1]
                sales = self.calculate_sales(current_volume, previous_volume=previous_volume)
                DailyTankSales.objects.create(tank_id=tank_id, date=created_at_date, sales=max(sales, 0))

    def create_daily_tank_sales(self, tank_volume):
        tank_id = tank_volume.tank_id
        created_at_date = tank_volume.created_at.date()

        # Get the previous volume record for the same tank and date
        previous_volume = TankVolume.objects.filter(
            tank_id=tank_id,
            created_at__date=created_at_date,
            created_at__lt=tank_volume.created_at
        ).order_by('-created_at').first()

        if previous_volume:
            # If a previous volume record exists for the same date
            sales = self.calculate_sales(tank_volume, previous_volume=previous_volume)
            DailyTankSales.objects.create(tank_id=tank_id, date=created_at_date, sales=max(sales, 0))
        else:
            # If no previous volume record exists for the same date, check the previous day's last volume
            previous_day_last_volume = TankVolume.objects.filter(
                tank_id=tank_id,
                created_at__date=created_at_date - timedelta(days=1)
            ).order_by('-created_at').first()

            if previous_day_last_volume:
                # If the previous day's last volume exists, calculate the sales
                sales = self.calculate_sales(tank_volume, previous_day_last_volume=previous_day_last_volume)
                DailyTankSales.objects.create(tank_id=tank_id, date=created_at_date, sales=max(sales, 0))
            else:
                # If no previous day's last volume exists, it means this is the first volume record for the tank
                # In this case, we don't create a DailyTankSales record
                pass


class RunningAverageSalesView(APIView):
    def get(self, request, tank_id, date):
        target_date = datetime.strptime(date, '%Y-%m-%d').date()
        end_date = target_date
        start_date = end_date - timedelta(weeks=4)

        daily_sales = DailyTankSales.objects.filter(tank_id=tank_id, date__range=[start_date, end_date])

        total_sales = daily_sales.aggregate(total_sales=Sum('sales'))['total_sales'] or 0
        num_records = daily_sales.count()
        average_sales = total_sales / num_records if num_records > 0 else 0

        return Response({
            'tank_id': tank_id,
            'date': target_date,
            'number_of_sales': num_records,
            'average_sales': average_sales
        })


class DailyTanksViewSet(viewsets.ModelViewSet):
    queryset = DailyTankSales.objects.all()
    serializer_class = DailyTankSerializer


class TankVolumeLookupView(APIView):
    def get(self, request):
        date_str = request.query_params.get('date')
        datetime_str = request.query_params.get('datetime')

        if date_str:
            target_date = parse_date(date_str)
            if not target_date:
                return Response({"error": "Invalid date format"}, status=400)
            volumes = TankVolume.objects.filter(created_at__date=target_date)
        elif datetime_str:
            target_datetime = parse_datetime(datetime_str)
            if not target_datetime:
                return Response({"error": "Invalid datetime format"}, status=400)
            volumes = TankVolume.objects.filter(created_at=target_datetime)
        else:
            return Response({"error": "Date or datetime query parameter is required"}, status=400)

        serializer = TankVolumeSerializer(volumes, many=True, context={'request': request})
        return Response(serializer.data)
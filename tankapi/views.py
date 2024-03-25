from datetime import datetime, timedelta
from django.db.models import Sum
from django.utils.dateparse import parse_date, parse_datetime
from rest_framework import viewsets, permissions
from .models import Tank, TankVolume, DailyTankSales
from .serializers import TankSerializer, TankVolumeSerializer, DailyTankSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
import logging

logger = logging.getLogger(__name__)


class TankViewSet(viewsets.ModelViewSet):
    """
    Api endpoint that allows Tanks to be viewed or edited. CRUD
    """
    queryset = Tank.objects.all()
    serializer_class = TankSerializer
    permission_classes = [permissions.AllowAny]  # This would be isAuthenticated in production


class TankVolumeViewSet(viewsets.ModelViewSet):
    """
    Api endpoint that allows Tanks to be created, viewed, or edited. CRUD
    """
    queryset = TankVolume.objects.all()
    serializer_class = TankVolumeSerializer
    permission_classes = [permissions.AllowAny]  # same authentication note as above

    def perform_create(self, serializer):
        instance = serializer.save()
        self.create_daily_tank_sales(instance)

    def perform_update(self, serializer):
        instance = serializer.save()
        self.update_tank_volume_and_daily_sales(instance)

    def update_tank_volume_and_daily_sales(self, instance):
        # logger.debug(f"update_tank_volume_and_daily_sales called for TankVolume: {instance}")
        tank_id = instance.tank_id

        if isinstance(instance.created_at, str):
            created_at = datetime.strptime(instance.created_at, '%Y-%m-%dT%H:%M:%SZ')
        else:
            created_at = instance.created_at

        created_at_date = created_at.date()

        # logger.debug(f"Processing TankVolume instance: {instance}")
        # logger.debug(f"Tank ID: {tank_id}")
        # logger.debug(f"Created At Date: {created_at_date}")

        # Delete all DailyTankSales records for the same tank and date
        DailyTankSales.objects.filter(tank_id=tank_id, date=created_at_date).delete()
        # logger.debug(f"Deleted DailyTankSales records for tank {tank_id} on {created_at_date}")

        # Get all TankVolume records for the same tank and date
        tank_volumes = TankVolume.objects.filter(tank_id=tank_id, created_at__date=created_at_date).order_by(
            'created_at')

        # Recalculate DailyTankSales for each TankVolume record
        for i in range(len(tank_volumes)):
            current_volume = tank_volumes[i]
            # logger.debug(f"Processing TankVolume: {current_volume}")

            if i == 0:
                # If it's the first volume of the day, check the previous day's last volume
                previous_day_last_volume = TankVolume.objects.filter(
                    tank_id=tank_id,
                    created_at__date=created_at_date - timedelta(days=1)
                ).order_by('-created_at').first()

                if previous_day_last_volume:
                    # logger.debug(f"Previous day's last volume: {previous_day_last_volume}")
                    sales = current_volume.volume - previous_day_last_volume.volume
                    # logger.debug(f"Calculated sales using previous day's last volume: {sales}")
                else:
                    # logger.debug("No previous day's last volume found")
                    sales = 0
            else:
                # If it's not the first volume of the day, calculate the sales using the previous volume
                previous_volume = tank_volumes[i - 1]
                # logger.debug(f"Previous volume: {previous_volume}")
                sales = current_volume.volume - previous_volume.volume
                # logger.debug(f"Calculated sales using previous volume: {sales}")

            if sales > 0:
                DailyTankSales.objects.create(tank_id=tank_id, date=created_at_date, sales=sales)
                # logger.debug(f"Created DailyTankSales record with sales: {sales}")
            elif sales < 0:
                daily_sales = DailyTankSales.objects.create(tank_id=tank_id, date=created_at_date, sales=0)
                # logger.debug(f"Created DailyTankSales: {daily_sales}")
            else:
                logger.debug(f"Created DailyTankSales record with zero sales")

        print("---")

    def create_daily_tank_sales(self, instance):
        # logger.debug(f"create_daily_tank_sales called for TankVolume: {instance}")
        tank_id = instance.tank_id

        if isinstance(instance.created_at, str):
            created_at = datetime.strptime(instance.created_at, '%Y-%m-%dT%H:%M:%SZ')
        else:
            created_at = instance.created_at

        created_at_date = created_at.date()

        # logger.debug(f"Processing TankVolume instance: {instance}")
        # logger.debug(f"Tank ID: {tank_id}")
        # logger.debug(f"Created At Date: {created_at_date}")

        # Get the previous volume record for the same tank and date
        previous_volume = TankVolume.objects.filter(
            tank_id=tank_id,
            created_at__date=created_at_date,
            created_at__lt=instance.created_at
        ).order_by('-created_at').first()

        # logger.debug(f"Previous Volume: {previous_volume}")

        if previous_volume:
            # If a previous volume record exists for the same date
            sales = instance.volume - previous_volume.volume

            if sales > 0:
                # If the sales are positive, create a new DailyTankSales record
                # logger.debug(f"Sales calculated using previous volume: {sales}")
                daily_sales = DailyTankSales.objects.create(tank_id=tank_id, date=created_at_date, sales=sales)
                # logger.debug(f"Created DailyTankSales: {daily_sales}")
            elif sales < 0:
                # If the sales are negative, create a new DailyTankSales record with zero sales
                # logger.debug(f"Negative sales calculated using previous volume: {sales}")
                daily_sales = DailyTankSales.objects.create(tank_id=tank_id, date=created_at_date, sales=0)
                # logger.debug(f"Created DailyTankSales with zero sales: {daily_sales}")
            else:
                logger.debug("No sales. Skipping DailyTankSales creation.")
        else:
            # If no previous volume record exists for the same date, check the previous day's last volume
            previous_day_last_volume = TankVolume.objects.filter(
                tank_id=tank_id,
                created_at__date__lt=created_at_date
            ).order_by('-created_at').first()

            if previous_day_last_volume and previous_day_last_volume.created_at.date() == created_at_date - timedelta(
                    days=1):
                # If the previous day's last volume is from the immediately previous day, calculate the sales
                sales = instance.volume - previous_day_last_volume.volume
                # logger.debug(f"Sales calculated using previous day's last volume: {sales}")
            else:
                # If no previous day's last volume exists or it's from an earlier date, set the sales to 0
                sales = 0
                # logger.debug("No valid previous volume found, sales set to 0")

            if sales > 0:
                # Create a new DailyTankSales record for each positive sales value
                daily_sales = DailyTankSales.objects.create(tank_id=tank_id, date=created_at_date, sales=sales)
                # logger.debug(f"Calculated Sales: {sales}")
                # logger.debug(f"Created DailyTankSales: {daily_sales}")
            elif sales < 0:
                daily_sales = DailyTankSales.objects.create(tank_id=tank_id, date=created_at_date, sales=0)
                # logger.debug(f"Created DailyTankSales: {daily_sales}")
            else:
                logger.debug(f"zero")

        print("---")


class RunningAverageSalesView(APIView):
    """
    How we deliver the weekly average.
    """

    def get(self, request, tank_id, date):
        # Get the date from the URL
        target_date = datetime.strptime(date, '%Y-%m-%d').date()

        # Calculate the start and end dates
        end_date = target_date
        start_date = end_date - timedelta(weeks=4)

        # Get the daily tank sales
        daily_sales = DailyTankSales.objects.filter(tank_id=tank_id, date__range=[start_date, end_date])

        logger.debug("Daily Sales: %s", daily_sales)
        logger.debug("Start Date: %s", start_date)
        logger.debug("End Date: %s", end_date)

        # Calculate the total sales and count the number of sales records
        total_sales = daily_sales.aggregate(total_sales=Sum('sales'))['total_sales'] or 0
        num_records = daily_sales.count()

        if num_records > 0:
            average_sales = total_sales / num_records
        else:
            average_sales = 0

        sales_data = {sales.date: sales.sales for sales in daily_sales}

        logger.debug("Total Sales: %s", total_sales)
        logger.debug("Number of Records: %s", num_records)
        logger.debug("Average Sales: %s", average_sales)
        logger.debug("Daily Sales: %s", sales_data)

        return Response({'tank_id': tank_id, 'date': target_date, 'number_of_sales': num_records,
                         'average_sales': average_sales})


class DailyTanksViewSet(viewsets.ModelViewSet):
    queryset = DailyTankSales.objects.all()
    serializer_class = DailyTankSerializer
    permission_classes = [permissions.AllowAny]


class TankVolumeLookup(APIView):
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

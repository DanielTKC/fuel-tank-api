from rest_framework import viewsets, permissions
from .models import Tank, TankVolume
from .serializers import TankSerializer, TankVolumeSerializer


class TankViewSet(viewsets.ModelViewSet):
    """
    Api endpoint that allows Tanks to be viewed or edited
    """
    queryset = Tank.objects.all()
    serializer_class = TankSerializer
    permission_classes = [permissions.AllowAny]  # This would be isAuthenticated in production


class TankVolumeViewSet(viewsets.ModelViewSet):
    """
    Api endpoint that allows Tanks to be viewed or edited
    """
    queryset = TankVolume.objects.all()
    serializer_class = TankVolumeSerializer
    permission_classes = [permissions.AllowAny]  # same note as above

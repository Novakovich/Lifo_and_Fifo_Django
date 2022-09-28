from rest_framework import viewsets
from rest_framework import permissions
from donation.models import Description, DonateItem
from tutorial.quickstart.serializers import DescriptionSerializer, DonateItemSerializer


class DescriptionViewSet(viewsets.ModelViewSet):
    queryset = Description.objects.all().order_by('-id')
    serializer_class = DescriptionSerializer
    permission_classes = [permissions.IsAuthenticated]


class DonateItemViewSet(viewsets.ModelViewSet):
    queryset = DonateItem.objects.all()
    serializer_class = DonateItemSerializer
    permission_classes = [permissions.IsAuthenticated]

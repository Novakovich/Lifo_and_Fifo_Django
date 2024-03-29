from rest_framework import viewsets, generics
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


class DescriptionList(generics.ListCreateAPIView):
    queryset = Description.objects.all()
    serializer_class = DescriptionSerializer

    def get_queryset(self):
        return super().get_queryset().filter(donate_uuid=self.kwargs['donate_uuid'])

    def perform_create(self, serializer):
        serializer.save(donate_uuid_id=self.kwargs['donate_uuid'])

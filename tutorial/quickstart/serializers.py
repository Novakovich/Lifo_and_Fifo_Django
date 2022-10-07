from rest_framework import serializers
from donation.models import Description, DonateItem


class DescriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Description
        exclude = ['donate_uuid', ]


class DonateItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = DonateItem
        fields = '__all__'

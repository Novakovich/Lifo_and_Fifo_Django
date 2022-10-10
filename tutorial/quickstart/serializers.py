from rest_framework import serializers
from donation.models import Description, DonateItem


class DescriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Description
        fields = '__all__'


class DonateItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = DonateItem
        fields = '__all__'

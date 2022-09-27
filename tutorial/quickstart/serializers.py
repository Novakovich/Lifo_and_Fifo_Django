from rest_framework import serializers

from donation.models import Description, DonateItem


class DescriptionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Description
        fields = ['id', 'details', 'condition', 'place']


class DonateItemSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = DonateItem
        fields = ['name', 'id', 'state', 'donate_uuid', 'amount_item', 'office_id']

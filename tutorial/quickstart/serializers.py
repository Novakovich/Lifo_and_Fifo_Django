from rest_framework import serializers
from donation.models import Description, DonateItem


class DescriptionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Description
        fields = [
            'id', 'name_item', 'amount_item', 'office_id', 'state', 'details', 'condition', 'place', 'donate_uuid_id',
                  ]


class DonateItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = DonateItem
        fields = ['name_item', 'id', 'state', 'donate_uuid', 'amount_item', 'office_id']

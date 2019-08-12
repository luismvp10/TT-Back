from rest_framework import serializers
from subshipments.models import Subshipment

class SubshipmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subshipment
        fields=('id_subShipment', 'name')
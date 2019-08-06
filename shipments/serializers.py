from rest_framework import serializers
from shipments.models import Shipment

class ShipmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shipment
        fields=('id_shipment','name')
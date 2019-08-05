from rest_framework import serializers
from transactions.models import Transaction

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields=('id_transacion','price', 'weight', 'id_kind', 'id_country','id_section','id_subShipment', 'id_shipment', 'id_chapter', 'id_year', 'id_month')
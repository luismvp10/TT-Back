from rest_framework import serializers
from transactions.models import Transaction

class TransactionSerializer(serializers.ModelSerializer):
    #id_transaction = serializers.ReadOnlyField(allow_null=True)
    #price = serializers.ReadOnlyField(allow_null=True)
    #weight = serializers.ReadOnlyField(allow_null=True)
    #section = serializers.ReadOnlyField(source='section.name',allow_null=True)
    #year = serializers.ReadOnlyField(source='year.name',allow_null=True)
    #month = serializers.ReadOnlyField(source='month.name',allow_null=True)
    class Meta:
        model = Transaction
        fields=('id_transaction', 'price', 'weight', 'year', 'month')

class CustomSerializer(serializers.Serializer):
    country = serializers.CharField(max_length=50)
    imports = TransactionSerializer(many=True)
    exports = TransactionSerializer(many=True)

class TransactionsSerializer(serializers.Serializer):
    price = serializers.FloatField()
    weight = serializers.FloatField()
    month = serializers.IntegerField()

class ShipmentSerializer(serializers.Serializer):
    country = serializers.CharField(max_length=50)
    imports = TransactionsSerializer(many=True)
    exports = TransactionsSerializer(many=True)
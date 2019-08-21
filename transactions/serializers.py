from rest_framework import serializers
from transactions.models import Transaction

class TransactionSerializer(serializers.ModelSerializer):
    kind = serializers.ReadOnlyField(source='kind.name')
    country = serializers.ReadOnlyField(source='country.name')
    section = serializers.ReadOnlyField(source='section.name')
    year = serializers.ReadOnlyField(source='year.name')
    month = serializers.ReadOnlyField(source='month.name')
    class Meta:
        model = Transaction
        fields=('id_transaction', 'price', 'weight', 'kind', 'country', 'section', 'year', 'month')
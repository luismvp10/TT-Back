from rest_framework import serializers
from months.models import Month

class MonthSerializer(serializers.ModelSerializer):
    class Meta:
        model = Month
        fields=('id_month','name')
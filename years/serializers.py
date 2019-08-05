from rest_framework import serializers
from years.models import Year

class YearSerializer(serializers.ModelSerializer):
    class Meta:
        model = Year
        fields=('id_year','name')
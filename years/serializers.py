from rest_framework import serializers
from years.models import Year
# from years.models import Year_has_month

class YearSerializer(serializers.ModelSerializer):
    class Meta:
        model = Year
        fields=('id_year', 'name')
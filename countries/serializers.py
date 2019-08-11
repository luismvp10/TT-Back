from rest_framework import serializers
from countries.models import Countrie

class CountrieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Countrie
        fields=('id_country','name','iso2','iso3')
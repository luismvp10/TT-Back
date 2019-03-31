from rest_framework import serializers
from countries.models import Countrie

class CountrieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Countrie
        fields=('id','name','iso2','iso3')
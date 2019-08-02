from rest_framework import serializers
from units.models import Unity

class UnitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Unity
        fields = ('id_unity','name')
from rest_framework import serializers
from users.models import User
# from years.models import Year_has_month

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields=('names', 'surname', 'email', 'user_type')
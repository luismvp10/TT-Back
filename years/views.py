from django.shortcuts import render
from rest_framework import generics
from years.models import Year
from years.serializers import YearSerializer
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny

# Create your views here.
@permission_classes((AllowAny,))
class YearList(generics.ListAPIView):
    queryset = Year.objects.order_by('id_year')[::-1]
    serializer_class = YearSerializer
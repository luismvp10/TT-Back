from django.shortcuts import render
from rest_framework import generics
from months.models import Month
from months.serializers import MonthSerializer


# Create your views here.
class MonthList(generics.ListAPIView):
    queryset = Month.objects.order_by('id_month');
    serializer_class = MonthSerializer
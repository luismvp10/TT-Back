from django.shortcuts import render
from rest_framework import generics


from months.models import Month
from months.serializers import MonthSerializer
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny

# Create your views here.
@permission_classes((AllowAny,))
class MonthList(generics.ListAPIView):
    queryset = Month.objects.order_by('id_month')
    serializer_class = MonthSerializer
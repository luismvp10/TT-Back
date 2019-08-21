from django.shortcuts import render
from rest_framework import generics
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny

from transactions.models import Transaction
from transactions.serializers import TransactionSerializer


# Create your views here.
@permission_classes((AllowAny,))
class TransactionList(generics.ListAPIView):
    serializer_class = TransactionSerializer

    def get_queryset(self):
        section = self.kwargs['section']
        country = self.kwargs['country']
        month = self.kwargs['month']
        year = self.kwargs['year']
        if month is None and country is None:
            return Transaction.objects.filter(section=section, year=year).select_related('year')
        if month is None and country is not None:
            return Transaction.objects.filter(section=section, year=year, country=country)
        if country is None and month is not None:
            return Transaction.objects.filter(section=section, year=year, month=month)
        else:
            return Transaction.objects.filter(section=section, year=year, month=month, country=country)
from django.http import HttpResponse
from rest_framework import generics
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny
from transactions.models import Transaction
from transactions.serializers import CustomSerializer


@permission_classes((AllowAny,))
class TransactionList(generics.ListAPIView):
    serializer_class = CustomSerializer

    def get_queryset(self):
        section = self.kwargs['section']
        country = self.kwargs['country']
        month = self.kwargs['month']
        year = self.kwargs['year']
        if month is None and country is None:
            query = Transaction.objects.filter(section=section, year=year)
            return groupquery(query)
        if month is None and country is not None:
            query = Transaction.objects.filter(section=section, year=year, country=country)
            return groupquery(query)
        if country is None and month is not None:
            query = Transaction.objects.filter(section=section, year=year, month=month)
            return groupquery(query)
        else:
            query = Transaction.objects.filter(section=section, year=year, month=month, country=country)
            return groupquery(query)

def groupquery(query):
    result = []
    i = -1
    for t in query:
        if country_exist(result, t.country.name):
            result.append({'country': t.country.name, 'transacciones': {t, }})
            i = i + 1
        else:
            result[i]['transacciones'].add(t)
    return result


def country_exist(array, country):
    if len(array) == 0:
        return True
    for a in range(len(array)):
        if array[a]['country'] == country:
            return False
    return True

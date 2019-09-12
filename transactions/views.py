from django.db.models import Count, Sum
from rest_framework import generics
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny
from transactions.models import Transaction
from transactions.serializers import CustomSerializer,ShipmentSerializer
from countries.models import Countrie

@permission_classes((AllowAny,))
class TransactionList(generics.ListAPIView):
    serializer_class = CustomSerializer

    def get_queryset(self):
        section = self.kwargs['section']
        country = self.kwargs['country']
        month = self.kwargs['month']
        year = self.kwargs['year']
        data = month.split()  # split string into a list
        months = []
        for temp in data:
            months.append(temp)
        if month is None and country is None:
            query = Transaction.objects.filter(section=section, year=year).values('country').annotate(Count('country'))
            return groupquery(query,section,year)
        if month is None and country is not None:
            query = Transaction.objects.filter(section=section, year=year, country=country).values('country').annotate(Count('country'))
            return groupquery(query,section,year)
        if country is None and month is not None:
            query = Transaction.objects.filter(section=section, year=year, month__in=months).values('country').annotate(Count('country'))
            return groupquery(query,section,year,month=months)
        else:
            query = Transaction.objects.filter(section=section, year=year, month__in=months, country=country).values('country').annotate(Count('country'))
            return groupquery(query,section,year,month=months)


@permission_classes((AllowAny,))
class TransactionSubshipment(generics.ListAPIView):
    serializer_class = ShipmentSerializer

    def get_queryset(self):
        operation = self.kwargs['operation']
        country = self.kwargs['country']
        month = self.kwargs['month']
        year = self.kwargs['year']
        if month is not None:
            data = month.split()
            months = []
            for temp in data:
                months.append(temp)
        if month is None and country is None:
            query = Transaction.objects.filter(section__id_section__contains=operation, year=year).values('country').annotate(Count('country'))
            return sumquery(query,operation,year)
        if month is None and country is not None:
            query = Transaction.objects.filter(section__id_section__contains=operation, year=year, country=country).values('country').annotate(Count('country'))
            return sumquery(query,operation,year)
        if country is None and month is not None:
            query = Transaction.objects.filter(section__id_section__contains=operation, year=year, month__in=months).values('country').annotate(Count('country'))
            return sumquery(query,operation,year,month=months)
        else:
            query = Transaction.objects.filter(section__id_section__contains=operation, year=year, month__in=months, country=country).values('country').annotate(Count('country'))
            return sumquery(query,operation,year,month=months)


def groupquery(query,section,year,**kwargs):
    month=kwargs.get('month')
    result = []
    for x in query:
        c = Countrie.objects.get(id_country=x['country'])
        if month is not None:
            q = Transaction.objects.filter(section=section, year=year, country=x['country'], month__in=month, kind=1).order_by('month')
            imports = list(q)
            q = Transaction.objects.filter(section=section, year=year, country=x['country'], month__in=month, kind=2).order_by('month')
            exports = list(q)
        else:
            q = Transaction.objects.filter(section=section, year=year, country=x['country'], kind=1).order_by('month')
            imports = list(q)
            q = Transaction.objects.filter(section=section, year=year, country=x['country'], kind=2).order_by('month')
            exports = list(q)
        result.append({'country': c.name, 'imports': imports, 'exports': exports})
    return result

def sumquery(query,operation,year,**kwargs):
    month=kwargs.get('month')
    result = []
    for x in query:
        c = Countrie.objects.get(id_country=x['country'])
        if month is not None:
            q = Transaction.objects.filter(section__id_section__contains=operation, year=year,
                                           country=x['country'], month__in=month, kind=1).values('month').annotate(
                price=Sum('price'),
                weight=Sum(
                    'weight')).order_by('month')
            imports = list(q)
            q = Transaction.objects.filter(section__id_section__contains=operation, year=year,
                                           country=x['country'], month__in=month, kind=2).values('month').annotate(
                price=Sum('price'),
                weight=Sum(
                    'weight')).order_by('month')
            exports = list(q)
        else:
            q = Transaction.objects.filter(section__id_section__contains=operation, year=year,
                                           country=x['country'], kind=1).values('month').annotate(
                price=Sum('price'),
                weight=Sum(
                    'weight')).order_by('month')
            imports = list(q)
            q = Transaction.objects.filter(section__id_section__contains=operation, year=year,
                                           country=x['country'], kind=2).values('month').annotate(
                price=Sum('price'),
                weight=Sum(
                    'weight')).order_by('month')
            exports = list(q)
        result.append({'country': c.name, 'imports':imports, 'exports':exports})
    return result


from django.http import HttpResponse


def hello_world(request,month):
    data = month.split()  # split string into a list
    months=[]
    for temp in data:
        months.append(temp)
    query = Transaction.objects.filter(section__id_section__contains="75", year=16, kind=2, month__in =months).values('month')
    print(query)
    return HttpResponse('Hola Mundo')

from django.db.models import Count, Sum
from rest_framework import generics
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny
from sklearn.linear_model import LinearRegression
from tkinter import Image
from transactions.models import Transaction
from transactions.serializers import CustomSerializer,ShipmentSerializer
from countries.models import Countrie
from sklearn.preprocessing import PolynomialFeatures as Polinomizar
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from pandas.plotting import register_matplotlib_converters
import matplotlib
from datetime import datetime
plt.style.use('seaborn')
register_matplotlib_converters()

@permission_classes((AllowAny,))
class TransactionList(generics.ListAPIView):
    serializer_class = CustomSerializer

    def get_queryset(self):
        section = self.kwargs['section']
        country = self.kwargs['country']
        month = self.kwargs['month']
        year = self.kwargs['year']
        if month is not None:
            data = month.split()
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

def prediction(request,operation, kind, country):

    if country is None:
        t = Transaction.objects.filter(section__id_section__contains=operation, year__id_year__range=(12, 16),
                                       kind=kind).values_list('month', 'year').annotate(
            price=Sum('price'),
            weight=Sum('weight')).order_by('kind', 'year', 'month')
    else:
        t = Transaction.objects.filter(section__id_section__contains=operation, year__id_year__range=(12, 16),
                                       kind=kind,
                                       country=country).values_list('month', 'year').annotate(
            price=Sum('price'),
            weight=Sum('weight')).order_by('kind', 'year', 'month')
    df = pd.DataFrame(list(t), columns=['month', 'year', 'price', 'weight'])
    df.year = df.year.replace([12, 13, 14, 15, 16], [2014, 2015, 2016, 2017, 2018])
    X = df.index
    y = df.price
    df['Date'] = pd.to_datetime([f'{y}-{m}-01' for y, m in zip(df.year, df.month)])
    df.set_index('Date', inplace=True)
    polinomizador = Polinomizar(degree=4)
    X = polinomizador.fit_transform(X.values.reshape(-1, 1))
    ny = []
    for i in range(1, 7):
        ny.append(len(df.price) + i)
    x_test = polinomizador.fit_transform(np.array(ny).reshape(-1, 1))
    regressor = LinearRegression()
    regressor.fit(X, y)
    y_fit = regressor.predict(X)
    y_test = regressor.predict(x_test)
    print(regressor.score(X, y))
    matplotlib.use('Agg')
    predictDate = []
    for i in range(6):
        if (i == 0):
            predictDate.append(addMonth(df.last_valid_index()))
        else:
            predictDate.append(addMonth(predictDate[i - 1]))
    for i in range(6):
        if y_test[i] < 0:
            y_test[i] = 0
    #_2019 = [420, 2548, 205390, 155914, 262567, 259913 ]
    plt.plot(df.price, marker='o', markerfacecolor='blue', color='skyblue', linewidth=3, label='Valor real')
    plt.plot(df.index, y_fit, color='orange', label='Linea de tendencia')
    plt.plot(predictDate, y_test, marker='o', color='#2DAB20', label='Valor esperado')
    #plt.plot(predictDate, _2019, marker='o', color='#2DAB20')
    plt.ticklabel_format(style='plain', axis='y')
    plt.legend()
    plt.xlabel('Años')
    plt.ylabel('Valor en dolares')
    plt.savefig("regresionpolinomica.png")
    plt.close()
    try:
        with open("regresionpolinomica.png", "rb") as f:
            return HttpResponse(f.read(), content_type="image/jpeg")
    except IOError:
        red = Image.new('RGBA', (1, 1), (255, 0, 0, 0))
        response = HttpResponse(content_type="image/jpeg")
        red.save(response, "JPEG")
        return response

def addMonth(date):
    year, month = divmod(date.month + 1, 12)
    if month == 0:
        month = 12
        year = year - 1
    return datetime(date.year + year, month, 1)

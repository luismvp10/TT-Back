from django.db.models import Count, Sum
from rest_framework import generics
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny
from sklearn.linear_model import LinearRegression
from tkinter import Image
from transactions.models import Transaction
from transactions.serializers import CustomSerializer, ShipmentSerializer
from countries.models import Countrie
from sklearn.preprocessing import PolynomialFeatures as Polinomizar
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import json
from reportlab.lib.units import inch
from pandas.plotting import register_matplotlib_converters
import matplotlib
from datetime import datetime
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_200_OK
)
from reportlab.platypus.tables import Table
from reportlab.platypus import (SimpleDocTemplate, PageBreak, Image, Spacer,
                                Paragraph, Table, TableStyle)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.pagesizes import landscape, letter
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from textwrap import wrap

plt.style.use('seaborn')
register_matplotlib_converters()
pageinfo = "platypus example"

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
            return groupquery(query, section, year)
        if month is None and country is not None:
            query = Transaction.objects.filter(section=section, year=year, country=country).values('country').annotate(
                Count('country'))
            return groupquery(query, section, year)
        if country is None and month is not None:
            query = Transaction.objects.filter(section=section, year=year, month__in=months).values('country').annotate(
                Count('country'))
            return groupquery(query, section, year, month=months)
        else:
            query = Transaction.objects.filter(section=section, year=year, month__in=months, country=country).values(
                'country').annotate(Count('country'))
            return groupquery(query, section, year, month=months)


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
            query = Transaction.objects.filter(section__id_section__contains=operation, year=year).values(
                'country').annotate(Count('country'))
            return sumquery(query, operation, year)
        if month is None and country is not None:
            query = Transaction.objects.filter(section__id_section__contains=operation, year=year,
                                               country=country).values('country').annotate(Count('country'))
            return sumquery(query, operation, year)
        if country is None and month is not None:
            query = Transaction.objects.filter(section__id_section__contains=operation, year=year,
                                               month__in=months).values('country').annotate(Count('country'))
            return sumquery(query, operation, year, month=months)
        else:
            query = Transaction.objects.filter(section__id_section__contains=operation, year=year, month__in=months,
                                               country=country).values('country').annotate(Count('country'))
            return sumquery(query, operation, year, month=months)


def groupquery(query, section, year, **kwargs):
    month = kwargs.get('month')
    result = []
    for x in query:
        c = Countrie.objects.get(id_country=x['country'])
        if month is not None:
            q = Transaction.objects.filter(section=section, year=year, country=x['country'], month__in=month,
                                           kind=1).order_by('month')
            imports = list(q)
            q = Transaction.objects.filter(section=section, year=year, country=x['country'], month__in=month,
                                           kind=2).order_by('month')
            exports = list(q)
        else:
            q = Transaction.objects.filter(section=section, year=year, country=x['country'], kind=1).order_by('month')
            imports = list(q)
            q = Transaction.objects.filter(section=section, year=year, country=x['country'], kind=2).order_by('month')
            exports = list(q)
        result.append({'country': c.name, 'imports': imports, 'exports': exports})
    for q in result:
        tp = tw = 0
        for x in q['imports']:
            tp = tp + x['price']
            tw = tw + x['weight']
        if tp != 0 and tw != 0:
            q['imports'].append({'month': 13, 'price': tp, 'weight': tw})
        tp = tw = 0
        for x in q['exports']:
            tp = tp + x['price']
            tw = tw + x['weight']
        if tp != 0 and tw != 0:
            q['exports'].append({'month': 13, 'price': tp, 'weight': tw})
    return result


def sumquery(query, operation, year, **kwargs):
    month = kwargs.get('month')
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
        result.append({'country': c.name, 'imports': imports, 'exports': exports})
    for q in result:
        tp = tw = 0
        for x in q['imports']:
            tp = tp + x['price']
            tw = tw + x['weight']
        if len(q['imports']) != 0:
            q['imports'].append({'month': 13, 'price': tp, 'weight': tw})
        tp = tw = 0
        for x in q['exports']:
            tp = tp + x['price']
            tw = tw + x['weight']
        if len(q['exports']) != 0:
            q['exports'].append({'month': 13, 'price': tp, 'weight': tw})
    return result


from django.http import HttpResponse


def hello_world(request, month):
    data = month.split()  # split string into a list
    months = []
    for temp in data:
        months.append(temp)
    query = Transaction.objects.filter(section__id_section__contains="75", year=16, kind=2, month__in=months).values(
        'month')
    print(query)
    return HttpResponse('Hola Mundo')


def prediction(request, operation, kind, country):
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
    # _2019 = [420, 2548, 205390, 155914, 262567, 259913 ]
    plt.plot(df.price, marker='o', markerfacecolor='blue', color='skyblue', linewidth=3, label='Valor real')
    plt.plot(df.index, y_fit, color='orange', label='Linea de tendencia')
    plt.plot(predictDate, y_test, marker='o', color='#2DAB20', label='Valor esperado')
    # plt.plot(predictDate, _2019, marker='o', color='#2DAB20')
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


@csrf_exempt
@api_view(["GET"])
@permission_classes((AllowAny,))
def getReport(request, operation, country, month, year):
    if request.method == 'GET':
        cm = 2.54
        data = []
        if month is not None:
            data = month.split()
            months = []
            for temp in data:
                months.append(temp)
        print(months)
        if month is None and country is None:
            query = Transaction.objects.filter(section__id_section__contains=operation, year=year).values(
                'country').annotate(Count('country'))
            data = sumquery(query, operation, year)
        if month is None and country is not None:
            query = Transaction.objects.filter(section__id_section__contains=operation, year=year,
                                               country=country).values('country').annotate(Count('country'))
            data = sumquery(query, operation, year)
        if country is None and month is not None:
            query = Transaction.objects.filter(section__id_section__contains=operation, year=year,
                                               month__in=months).values('country').annotate(Count('country'))
            data = sumquery(query, operation, year, month=months)
        else:
            query = Transaction.objects.filter(section__id_section__contains=operation, year=year, month__in=months,
                                               country=country).values('country').annotate(Count('country'))
            data = sumquery(query, operation, year, month=months)
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename=reporte.pdf'

        elements = []

        doc = SimpleDocTemplate(response, pagesize=landscape(letter), rightMargin=0, leftMargin=0, topMargin=0.3 * cm,
                                bottomMargin=10*cm)
        stylesheet = getSampleStyleSheet()
        elements.append(Spacer(1, 5))
        elements.append(
            Paragraph('<align = "center"><font face="times" color="#8a0b0b" size= 20 '
                      '>&nbsp;&nbsp;c&nbsp;&nbsp;&nbsp;&nbsp;c&nbsp;&nbsp;&nbsp;&nbsp;SICAT</font> <font face="times" '
                      'color="#8a0b0b" size= 18 >"Sistema de Información Comercial para el Análisis de Transacciones" '
                      '</font> <align>',
                      stylesheet['Title']))
        elements.append(
            Paragraph('<align = "center"><font face="times" color="#3c92ca" size= 20 >Exportaciones </font> <align>',
                      stylesheet['Title']))
        elements.append(Paragraph(
            '<align = "left"><font face="times" size= 17 >&nbsp;&nbsp;&nbsp;&nbsp;Valor en dólares </font> <align>',
            stylesheet['Normal']))
        elements.append(Spacer(1, 25))
        elements.append(getTable(data, 'exports', 'price', months))
        elements.append(Spacer(1, 23))
        elements.append(PageBreak())
        elements.append(Paragraph(
            '<align = "left"><font face="times" size= 17 >&nbsp;&nbsp;&nbsp;&nbsp;Volumen </font> <align>',
            stylesheet['Normal']))
        elements.append(Spacer(1, 25))
        elements.append(getTable(data, 'exports', 'weight', months))
        elements.append(Spacer(1, 25))
        elements.append(PageBreak())
        elements.append(
            Paragraph('<align = "center"><font face="times" color="#3c92ca" size= 20 >Importaciones </font> <align>',
                      stylesheet['Title']))
        elements.append(Paragraph(
            '<align = "left"><font face="times" size= 17 >&nbsp;&nbsp;&nbsp;&nbsp;Valor en dólares </font> <align>',
            stylesheet['Normal']))
        elements.append(Spacer(1, 25))
        elements.append(getTable(data, 'imports', 'price', months))
        elements.append(Spacer(1, 23))

        elements.append(PageBreak())
        elements.append(Paragraph(
            '<align = "left"><font face="times" size= 17 >&nbsp;&nbsp;&nbsp;&nbsp;Volumen </font> <align>',
            stylesheet['Normal']))
        elements.append(Spacer(1, 25))
        elements.append(getTable(data, 'imports', 'weight', months))
        doc.build(elements,onFirstPage=myFirstPage , onLaterPages=myLaterPages)
        return response

def getTable(data, operation, kind, months):
    total = ['Total', 0]
    ta = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre',
          'Noviembre', 'Diciembre']
    temp = ['País',]
    for i in range(len(months)):
        total.append(0)
        temp.append(ta[int(months[i])-1])
    temp.append('Total')
    t=[temp]
    tam = 0
    for c in data:
        col = []
        wraped_text = "\n".join(wrap(c['country'], 10))
        col.append(wraped_text)
        i = 1
        for d in c[operation]:
            total[i] = total[i] + d[kind]
            if kind == 'price':
                col.append('$ ' + str(d[kind]))
            else:
                col.append(str(d[kind]) + ' kg')
            i = i + 1
        if len(col) > 1:
            t.append(col)
            tam = tam + 1
    i = 0
    tam = tam + 1
    for tot in total:
        if i > 0:
            if kind == 'price':
                total[i] = '$ ' + str(total[i])
            else:
                total[i] = str(total[i]) + ' kg'
        i = i + 1
    t.append(total)
    table = Table(t, colWidths=55)
    table.setStyle([
        ('GRID', (0, 0), (-1, -1), 1, colors.Color(red=(60.0 / 255), green=(146.0 / 255), blue=(202.0 / 255))),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('FONTSIZE', (0, 0), (-1, -1), 7.5),
        ('BACKGROUND', (0, 0), (-1, 0), colors.Color(red=(60.0 / 255), green=(146.0 / 255), blue=(202.0 / 255))),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGNMENT', (0, 0), (-1, -1), 'CENTER'),
        ('BACKGROUND', (0, 0), (-1, 0), colors.Color(red=(60.0 / 255), green=(146.0 / 255), blue=(202.0 / 255))),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('BACKGROUND', (0, tam), (-1, tam), colors.Color(red=(60.0 / 255), green=(146.0 / 255), blue=(202.0 / 255))),
        ('TEXTCOLOR', (0, tam), (-1, tam), colors.white),
    ])
    return table

def myLaterPages(canvas,doc):
    canvas.saveState()
    canvas.setFont('Times-Roman', 12)
    text = 'Nota:Los datos estadísticos de los últimos años, están sujetos a revisiones por parte del Grupo de Trabajo de Estadísticas de Comercio Exterior, integrado'
    text2 = 'por el Banco de México, INEGI, Servicio de Administración Tributaria y la Secretaría de Economía.'
    canvas.drawString(20, 20, "%s" % (text))
    canvas.drawString(20, 10, "%s" % (text2))
    canvas.restoreState()

def myFirstPage(canvas,doc):
    canvas.saveState()
    canvas.setFont('Times-Roman', 12)
    text = 'Nota:Los datos estadísticos de los últimos años, están sujetos a revisiones por parte del Grupo de Trabajo de Estadísticas de Comercio Exterior, integrado'
    text2 = 'por el Banco de México, INEGI, Servicio de Administración Tributaria y la Secretaría de Economía.'
    canvas.drawString(20, 20, "%s" % (text))
    canvas.drawString(20, 10, "%s" % (text2))
    canvas.drawInlineImage('sicat-logo.jpg', 40, 550, width=100, height=70)
    canvas.restoreState()
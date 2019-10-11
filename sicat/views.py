from tkinter import Image
import matplotlib
from django.db.models import Sum
from django.http import HttpResponse
from pandas import DataFrame
from sklearn import preprocessing
from sklearn.metrics import mean_squared_error
from transactions.models import Transaction
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import LogisticRegression
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from sklearn.preprocessing import PolynomialFeatures as Polinomizar
from sklearn.svm import SVR
from sklearn.preprocessing import MinMaxScaler
from sklearn.neural_network import MLPRegressor
from statsmodels.tsa.ar_model import AR
from datetime import datetime
from pandas.plotting import register_matplotlib_converters

plt.style.use('seaborn')
register_matplotlib_converters()


def regresion_lineal(request):
    t = Transaction.objects.filter(section__id_section__contains='75052101', year__id_year__range=(12, 16), kind=2,
                                   country=60).values_list('month', 'year').annotate(
        price=Sum('price'),
        weight=Sum(
            'weight')).order_by('kind', 'year', 'month')
    df = pd.DataFrame(list(t), columns=['month', 'year', 'price', 'weight'])
    df.year = df.year.replace([12, 13, 14, 15, 16], [2014, 2015, 2016, 2017, 2018])
    X = df.index
    y = df.weight
    df['Date'] = pd.to_datetime([f'{y}-{m}-01' for y, m in zip(df.year, df.month)])
    df.set_index('Date', inplace=True)
    regressor = LinearRegression()
    regressor.fit(X.values.reshape(-1, 1), y)
    prediccion_entrenamiento = regressor.predict(X.values.reshape(-1, 1))
    ny = []
    for i in range(1, 7):
        ny.append(len(df.price) + i)
    y_test = regressor.predict(np.array(ny).reshape(-1, 1))
    print(regressor.score(X.values.reshape(-1, 1), y))
    matplotlib.use('Agg')
    predictDate = []
    for i in range(6):
        if i == 0:
            predictDate.append(addMonth(df.last_valid_index()))
        else:
            predictDate.append(addMonth(predictDate[i - 1]))
    plt.plot(df.price, marker='o', markerfacecolor='blue', color='skyblue', linewidth=3)
    plt.plot(df.index, prediccion_entrenamiento, color='blue')
    plt.plot(predictDate, y_test, marker='o', color='#2DAB20')
    plt.title('Regresion lineal')
    plt.xlabel('Años')
    plt.ylabel('Valor en dolares')
    plt.savefig("regresionlineal.png")
    plt.close()
    try:
        with open("regresionlineal.png", "rb") as f:
            return HttpResponse(f.read(), content_type="image/jpeg")
    except IOError:
        red = Image.new('RGBA', (1, 1), (255, 0, 0, 0))
        response = HttpResponse(content_type="image/jpeg")
        red.save(response, "JPEG")
        return response


def regresion_polinomial(request):
    t = Transaction.objects.filter(section__id_section__contains='75052101', year__id_year__range=(12, 16), kind=2,
                                   country=60).values_list('month', 'year').annotate(
        price=Sum('price'),
        weight=Sum(
            'weight')).order_by('kind', 'year', 'month')
    df = pd.DataFrame(list(t), columns=['month', 'year', 'price', 'weight'])
    df.year = df.year.replace([12, 13, 14, 15, 16], [2014, 2015, 2016, 2017, 2018])
    X = df.index
    y = df.price
    df['Date'] = pd.to_datetime([f'{y}-{m}-01' for y, m in zip(df.year, df.month)])
    df.set_index('Date', inplace=True)
    polinomizador = Polinomizar(degree=5)
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
    _2019 = [7675838, 8426294, 5709494,	6746708, 7087399, 6204253 ]
    print(df.price.mean())
    plt.plot(df.price, marker='o', markerfacecolor='blue', color='skyblue', linewidth=3)
    plt.plot(df.index, y_fit, color='blue')
    plt.plot(predictDate, y_test, marker='o', color='#2DAB20')
    #plt.plot(predictDate, _2019, marker='o', color='green')
    plt.title('Regresión Polinómica')
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


def svr(request):
    t = Transaction.objects.filter(section__id_section__contains='75', year__id_year__range=(12, 16), kind=1,
                                   country=92).values_list('month', 'year').annotate(
        price=Sum('price'),
        weight=Sum(
            'weight')).order_by('kind', 'year', 'month')
    df = pd.DataFrame(list(t), columns=['month', 'year', 'price', 'weight'])
    df.year = df.year.replace([12, 13, 14, 15, 16], [2014, 2015, 2016, 2017, 2018])
    X = df.index
    y = df.price
    df['Date'] = pd.to_datetime([f'{y}-{m}-01' for y, m in zip(df.year, df.month)])
    df.set_index('Date', inplace=True)
    escaladorX = MinMaxScaler(feature_range=(0, 1))
    escaladorY = MinMaxScaler(feature_range=(0, 1))
    esc_X = escaladorX.fit_transform(X.values.reshape(-1, 1))
    esc_y = escaladorY.fit_transform(y.values.reshape(-1, 1))
    regresor_svr = SVR(kernel='rbf')
    regresor_svr.fit(esc_X, esc_y)
    y_fit = regresor_svr.predict(esc_X)
    ny = []
    for i in range(1, 7):
        ny.append(len(df.price) + i)
    test_pred = escaladorX.transform((np.array(ny).reshape(-1, 1)))
    y_test = regresor_svr.predict(test_pred)
    print(regresor_svr.score(esc_X, esc_y))
    y_test = escaladorY.inverse_transform(y_test.reshape(-1, 1))
    x_pred = escaladorX.transform(np.array([[37]]))
    y_pred = regresor_svr.predict(x_pred)
    y_fit = escaladorY.inverse_transform(y_fit.reshape(-1, 1))
    y_pred = escaladorY.inverse_transform(y_pred.reshape(-1, 1))
    predictDate = []
    for i in range(6):
        if (i == 0):
            predictDate.append(addMonth(df.last_valid_index()))
        else:
            predictDate.append(addMonth(predictDate[i - 1]))
    matplotlib.use('Agg')
    
    _2019 = [420, 2548, 205390, 155914, 262567, 259913 ]
    plt.plot(predictDate, _2019, marker='o', color='#2DAB20')
    plt.plot(df.price, marker='o', markerfacecolor='blue', color='skyblue', linewidth=3)
    plt.plot(df.index, y_fit, color='blue')
    plt.plot(predictDate, y_test, marker='o', color='#2DAB20')
    plt.title('SVR')
    plt.xlabel('Años')
    plt.ylabel('Valor en dolares')
    plt.savefig("SVR.png")
    plt.close()
    try:
        with open("SVR.png", "rb") as f:
            return HttpResponse(f.read(), content_type="image/jpeg")
    except IOError:
        red = Image.new('RGBA', (1, 1), (255, 0, 0, 0))
        response = HttpResponse(content_type="image/jpeg")
        red.save(response, "JPEG")
        return response


def arboles_decision(request):
    t = Transaction.objects.filter(section__id_section__contains='75052101', year__id_year__range=(12, 16), kind=2,
                                   country=60).values_list('month', 'year').annotate(
        price=Sum('price'),
        weight=Sum(
            'weight')).order_by('kind', 'year', 'month')
    df = pd.DataFrame(list(t), columns=['month', 'year', 'price', 'weight'])
    df.year = df.year.replace([12, 13, 14, 15, 16], [2014, 2015, 2016, 2017, 2018])
    print(df.head())
    df['Date'] = pd.to_datetime([f'{y}-{m}-01' for y, m in zip(df.year, df.month)])
    x = df.index
    y = df.price
    escaladorX = MinMaxScaler(feature_range=(0, 1))
    escaladorY = MinMaxScaler(feature_range=(0, 1))
    X_scaled = preprocessing.scale(y)
    escaldor = preprocessing.StandardScaler()
    ey = escaldor.fit_transform(y.values.reshape(-1, 1))
    polinomizador = Polinomizar(degree=5)
    X = polinomizador.fit_transform(x.values.reshape(-1, 1))
    ny = []
    for i in range(1, 7):
        ny.append(len(df.price) + i)
    x_test = polinomizador.fit_transform(np.array(ny).reshape(-1, 1))
    regressor = LinearRegression()
    regressor.fit(X, ey)
    y_fit = regressor.predict(X)
    y_test = regressor.predict(x_test)
    matplotlib.use('Agg')
    #plt.plot(df.price, color='blue', linestyle='-', marker='o')
    plt.plot(df.index , ey, color='blue', linestyle='-', marker='o')
    plt.title('Arboles de decision')
    plt.xlabel('Años')
    plt.ylabel('Valor en dolares')
    plt.savefig("arboles_desicion.png")
    plt.close()
    try:
        with open("arboles_desicion.png", "rb") as f:
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

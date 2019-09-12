from tkinter import Image
import matplotlib
from django.db.models import Sum
from django.http import HttpResponse
from pandas import DataFrame
from sklearn.metrics import mean_squared_error
from transactions.models import Transaction
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from sklearn.preprocessing import PolynomialFeatures as Polinomizar
from sklearn.svm import SVR
from sklearn.preprocessing import MinMaxScaler
from sklearn.tree import DecisionTreeRegressor as Arbol

def regresion_lineal(request):
    t = Transaction.objects.filter(section__id_section__contains='75089099', year__id_year__range=(14,16), kind=1, country=60).values_list('month', 'year').annotate(
                price=Sum('price'),
                weight=Sum(
                    'weight')).order_by('kind','year', 'month')
    df = pd.DataFrame(list(t), columns=['month', 'year', 'price', 'weight'])
    df = df.replace([14,15,16], [2016,2017,2018])
    df['index1'] = df.index+1
    X = df.iloc[0:36].index1
    y = df.iloc[0:36].weight
    regressor = LinearRegression()
    regressor.fit(X.values.reshape(-1, 1), y)
    prediccion_entrenamiento = regressor.predict(X.values.reshape(-1, 1))
    newyear = [37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48]
    y_test = regressor.predict(np.array(newyear).reshape(-1, 1))
    matplotlib.use('Agg')
    plt.scatter(X, y, color='red')
    plt.plot(X, prediccion_entrenamiento, color='blue')
    plt.scatter(newyear, y_test, color='#2DAB20')
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
    t = Transaction.objects.filter(section__id_section__contains='75089099', year__id_year__range=(14,16), kind=1, country=60).values_list('month', 'year').annotate(
                price=Sum('price'),
                weight=Sum(
                    'weight')).order_by('kind','year', 'month')
    df = pd.DataFrame(list(t), columns=['month', 'year', 'price', 'weight'])
    df = df.replace([14,15,16], [2016,2017,2018])
    df['index1'] = df.index+1
    X = df.iloc[0:36].index1
    y = df.iloc[0:36].weight
    polinomizador = Polinomizar(degree=3)
    X = polinomizador.fit_transform(X.values.reshape(-1, 1))
    newyear = [37,38,39,40,41,42,43,44,45,46,47,48]
    x_test =  polinomizador.fit_transform(np.array(newyear).reshape(-1, 1))
    regressor = LinearRegression()
    regressor.fit(X, y)
    y_fit = regressor.predict(X)
    y_test = regressor.predict(x_test)
    x = df.iloc[0:36].index1
    matplotlib.use('Agg')
    plt.scatter(x, y, color='red')
    plt.plot(x, y_fit, color='blue')
    plt.scatter(newyear, y_test, color='#2DAB20')
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
    t = Transaction.objects.filter(section__id_section__contains='75089099', year__id_year__range=(14,16), kind=1, country=60).values_list('month', 'year').annotate(
                price=Sum('price'),
                weight=Sum(
                    'weight')).order_by('kind','year', 'month')
    df = pd.DataFrame(list(t), columns=['month', 'year', 'price', 'weight'])
    df = df.replace([14,15,16], [2016,2017,2018])
    df['index1'] = df.index+1
    X = df.iloc[0:36].index1
    y = df.iloc[0:36].weight
    escaladorX = MinMaxScaler(feature_range=(0, 1))
    escaladorY = MinMaxScaler(feature_range=(0, 1))
    esc_X = escaladorX.fit_transform(X.values.reshape(-1,1))
    esc_y = escaladorY.fit_transform(y.values.reshape(-1,1))
    regresor_svr = SVR(kernel='rbf')
    regresor_svr.fit(esc_X, esc_y)
    y_fit = regresor_svr.predict(esc_X)
    newyear = [37,38,39,40,41,42,43,44,45,46,47,48]
    test_pred = escaladorX.transform((np.array(newyear).reshape(-1, 1)))
    y_test = regresor_svr.predict(test_pred)
    y_test = escaladorY.inverse_transform(y_test.reshape(-1, 1))
    x_pred = escaladorX.transform(np.array([[37]]))
    y_pred = regresor_svr.predict(x_pred)
    y_fit = escaladorY.inverse_transform(y_fit.reshape(-1, 1))
    y_pred = escaladorY.inverse_transform(y_pred.reshape(-1, 1))
    matplotlib.use('Agg')
    plt.scatter(X, y, color='red')
    plt.plot(X, y_fit, color='blue')
    plt.scatter(newyear, y_test, color='#2DAB20')
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
    t = Transaction.objects.filter(section__id_section__contains='75089099', year__id_year__range=(14,16), kind=1, country=60).values_list('month', 'year').annotate(
                price=Sum('price'),
                weight=Sum(
                    'weight')).order_by('kind','year', 'month')
    df = pd.DataFrame(list(t), columns=['month', 'year', 'price', 'weight'])
    df = df.replace([14,15,16], [2016,2017,2018])
    df['index1'] = df.index+1
    X = df.iloc[0:36].index1
    y = df.iloc[0:36].weight
    arbol = Arbol(criterion='mse')
    arbol.fit(X.values.reshape(-1,1), y)
    y_fit = arbol.predict(X.values.reshape(-1,1))
    x_pred = (np.array([[37]]))
    y_pred = arbol.predict(x_pred)
    X_grid = np.arange(min(X), max(X), 0.001)
    y_grid = arbol.predict(X_grid.reshape(-1, 1))
    matplotlib.use('Agg')
    plt.scatter(X, y, color='red')
    plt.plot(X_grid, y_grid, color='blue')
    plt.scatter(37, y_pred, color='#2DAB20')
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
from django.shortcuts import render
from .models import Calorie
import csv
from textblob import TextBlob
import math
from django.http import HttpResponse
import psycopg2 as pg2
import numpy as np
import pandas as pd
from tabulate import tabulate
# Create your views here.

def home(request):
    return render(request, 'home.html');

def Main(request):
    return render(request, 'Main.html');

def Calculate_Calorie(request):
    return render(request, 'Calculate_Calorie.html');

def load(request):

    # connect = pg2.connect(database='food',user= 'postgres',password= '0786')
    # cursor = connect.cursor()
    # cursor.execute('SELECT * FROM public.raw_interactions LIMIT 100')
    # res=cursor.fetchall()
    # for line in res:
    #     data.list = line[4]

    data = Calorie()
    connect = pg2.connect(database='food', user='postgres', password='0786')
    query = 'SELECT * FROM public.raw_recipe LIMIT 100'
    df = pd.read_sql(query, con=connect)
    df = pd.DataFrame(df, columns=['id', 'name'])
    df = df.head(10)
    df = df.to_numpy()
    headers = ["id", "name"]
    table = tabulate(df, headers, tablefmt="fancy_grid")
    data.list = table
    return render(request, "load.html",{'data':data});

def processing(request):
    pre = Calorie()
    connect = pg2.connect(database='food', user='postgres', password='0786')
    cursor = connect.cursor()
    cursor.execute('SELECT * FROM public.raw_interactions LIMIT 100')
    res = cursor.fetchall()
    for line in res:
        line = line[4]
        preprocecing = TextBlob(line)
        pre.pre = preprocecing.sentiment

    # connect = pg2.connect(database='food', user='postgres', password='0786')
    # query = 'SELECT * FROM public.raw_interactions LIMIT 100'
    # df = pd.read_sql(query, con=connect)
    # df = pd.DataFrame(df, columns=['review'])
    # df = df.head(10)
    # df = df.to_numpy()
    # headers = ["review"]
    # table = tabulate(df, headers, tablefmt="simple")
    # preprocecing = TextBlob(table)
    # pre.pre = preprocecing.sentiment

    return render(request, "processing.html",{'pre':pre});

def result(request):

    cal = Calorie()
    cal.name = str(request.POST['name'])
    cal.activity_level = str(request.POST['activity_level'])
    cal.weight = int(request.POST['weight'])
    cal.aim = str(request.POST['aim'])
    cal.food = str(request.POST['food'])
    cal.gender = str(request.POST['gender'])
    cal.age = int(request.POST['age'])
    cal.feet = float(request.POST['feet'])
    cal.inches = float(request.POST['inches'])

    cal.height = (cal.feet*30.48) + (cal.inches*2.54)



    if (cal.gender=='male'):
        bmr = 66.5 + (13.75 * cal.weight) + (5.003 * cal.height) + (6.755 * cal.age)
        if(cal.activity_level=='little'):
            cal.c = bmr * 1.2
        elif(cal.activity_level=='light'):
            cal.c = bmr * 1.375
        elif(cal.activity_level=='medium'):
            cal.c = bmr * 1.55
        elif(cal.activity_level=='high'):
            cal.c = bmr * 1.725
        else:
            cal.c = bmr * 1.9

    elif (cal.gender=='female'):
        bmr = 655.1 + (9.563 * cal.weight) + (1.850 * cal.height) + (4.676 * cal.age)
        if(cal.activity_level=='little'):
            cal.c = bmr * 1.2
        elif(cal.activity_level=='light'):
            cal.c = bmr * 1.375
        elif(cal.activity_level=='medium'):
            cal.c = bmr * 1.55
        elif(cal.activity_level=='high'):
            cal.c = bmr * 1.725
        else:
            cal.c = bmr * 1.9

    cal.c=round(cal.c, 2)

    # if (cal.aim == 'lose'):
    #     select * from table where




    return render(request, "result.html",{'cal':cal});
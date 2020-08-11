from django.shortcuts import render
from .models import Calorie
from textblob import TextBlob
import psycopg2 as pg2
import numpy as np
import pandas as pd
from tabulate import tabulate
from textblob import classifiers
from textblob.classifiers import NaiveBayesClassifier

def home(request):
    return render(request, 'home.html');

def Main(request):
    return render(request, 'Main.html');

def Calculate_Calorie(request):
    return render(request, 'Calculate_Calorie.html');

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
    global a,c,n,i
    a = cal.aim
    c = cal.c
    n = cal.food
    return render(request, "result.html",{'cal':cal});

def load(request):
    data = Calorie()
    aim = a
    cal = c
    rec = n.lower()
    connect = pg2.connect(database='food', user='postgres', password='0786')
    query = "SELECT * FROM raw_recipe"
    df = pd.read_sql(query, con=connect)
    df = pd.DataFrame(df, columns=['id', 'name', 'calories', 'ingredients'])
    if (aim == 'lose'):
        df = df[(df['calories'] <= cal) & (df.name.str.contains(rec))]
    if (aim == 'gain'):
        df = df[(df['calories'] >= cal) & (df.name.str.contains(rec))]
    if (aim == 'maintain'):
        df = df[(df['calories'] <= cal + 150) & (df['calories'] >= cal - 150) & (df.name.str.contains(rec))]
    df = df.head(30)
    # df = df.to_numpy()
    headers = ["Id", "Name", "Calories", "Ingredients"]
    table = tabulate(df, headers, tablefmt="fancy_grid", showindex=False)
    data.list = table
    return render(request, "load.html",{'data':data});

def processing(request):
    pre = Calorie()
    pre.desire = request.POST['desire']
    i = pre.desire
    id = int(i)
    global des
    des = id
    connect = pg2.connect(database='food', user='postgres', password='0786')
    # query = 'SELECT * FROM public.reviews'    //if we want to select and search through all data of user's interactions.
    query = 'SELECT * FROM public.interactions'
    df = pd.read_sql(query, con=connect)
    df = pd.DataFrame(df, columns=['recipe_id', 'rating', 'review'])
    df = df[df.recipe_id == id]
    df = df.head(10)
    headers = ["recipe_id", "rating", "review"]
    table = tabulate(df, headers, tablefmt="fancy_grid", showindex=False)
    pre.pre = table
    return render(request, "processing.html",{'pre':pre});

def sentiment(request):
    sent = Calorie()
    sent.desire = des
    id = int(sent.desire)
    connect = pg2.connect(database='food', user='postgres', password='0786')
    # query = 'SELECT * FROM public.reviews'    //if we want to select and search through all data of user's interactions.
    query = 'SELECT * FROM public.interactions'
    df = pd.read_sql(query, con=connect)
    df = pd.DataFrame(df, columns=['recipe_id', 'review'])
    df = df[df.recipe_id == id]
    df = df.head(10)
    df = df.to_string(index=False)
    blob = TextBlob(df).sentiment
    sent.sent = blob
    train = [
        ('Delicious!!! Great flavour and easy to prepare - this was a hit with the family. My only problem with the recipe is that you didnot state a temperature for the oven - I baked at 180C for about 40 minutes. Thanks for a great meal and good luck!!!', 'pos'),
        ('Excellent dish.  The topping is wonderfully rich and really makes the dish!', 'pos'),
        ('WOW!!! If I can please everyone at my table it is got to be GOOD.  This chicken had a wonderful flavor and was so simple to prepare.  Thank you.', 'pos'),
        ('I hate to be the bad apple in the bunch but my entire family was very disappointed. We thought the flavor was too bland. I ended up heating some soy/ginger sauce up and pouring it over it so that we could eat it. Very disappointed.', 'neg'),
        ('I am tired of this stuff.', 'neg'),
        ("I'm sorry, but I followed the directions exactly. The chicken was extremely tender, but the taste was worse than bland. I am using the leftovers in a casserole tonight. I will use the general idea again, but put seasoning on the chicken first. Thanks for sharing your recipe; maybe it's just a difference of taste!", 'neg'),
        ("Neither my kids or my husband were dazzled by this.  I made a pot pie out of the leftovers but the initial chicken was not a winner", "neg")
            ]
    cl = NaiveBayesClassifier(train)
    sent.pre = cl.classify(df)
    return render(request, "sentiment.html",{'sent':sent});

def show(request):
    final = Calorie()
    final.desire = des
    i = final.desire
    rec = int(i)
    connect = pg2.connect(database='food', user='postgres', password='0786')
    query = "SELECT * FROM raw_recipe"
    df = pd.read_sql(query, con=connect)
    df = pd.DataFrame(df, columns=['id', 'name', 'minutes', 'calories', 'fat', 'sugar', 'sodium', 'protein', 'saturated_fat', 'carbohydrates', 'description', 'n_ingredients', 'ingredients', 'ingredients', 'n_steps', 'steps'])
    df = df[df['id'] == rec]
    df = df.head(1)
    headers = ['Id', 'Name', 'Minutes', 'Calories', 'Fat', 'Sugar', 'Sodium', 'Protein', 'Saturated_Fat', 'Carbohydrates', 'Description', '# of Ingredients', 'Ingredients', 'Ingredients', '# of Steps', 'Steps']
    table = tabulate(df, headers, tablefmt="fancy_grid", showindex=False)
    final.show = table
    return render(request, "show.html",{'final':final});

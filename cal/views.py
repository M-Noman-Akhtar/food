from django.shortcuts import render
from .models import Calorie
import math
from django.http import HttpResponse
# Create your views here.

def home(request):
    return render(request, 'home.html');

def calorie(request):
    return render(request, 'cal.html');

def result(request):

    cal= Calorie()
    cal.name = str(request.POST['name'])
    cal.activity_level = str(request.POST['activity_level'])
    cal.weight = int(request.POST['weight'])
    cal.aim = str(request.POST['aim'])
    cal.food = str(request.POST['food'])
    cal.gender = str(request.POST['gender'])
    cal.age = int(request.POST['age'])
    cal.feet = float(request.POST['feet'])
    cal.inches = float(request.POST['inches'])

    cal.height= (cal.feet*30.48) + (cal.inches*2.54)



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
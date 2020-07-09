from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('Main', views.Main, name='Main'),
    path('Calculate_Calorie', views.Calculate_Calorie, name='Calculate_Calorie'),
    path('load', views.load, name='load'),
    path('processing', views.processing, name='processing'),
    path('result', views.result, name='result')
]

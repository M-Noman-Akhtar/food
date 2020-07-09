from django.db import models

# Create your models here.
class Calorie(models.Model):
    name = models.CharField(max_length=100)
    weight = models.IntegerField()
    aim = models.CharField(max_length=100)
    food = models.CharField(max_length=100)
    gender = models.CharField(max_length=100)
    age = models.IntegerField()
    feet = models.FloatField()
    inches = models.FloatField()
    c = models.FloatField()
    height = models.FloatField()
    list = models.CharField(max_length=500)
    pre = models.CharField(max_length=1000)
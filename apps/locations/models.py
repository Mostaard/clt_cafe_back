from django.db import models


class Location(models.Model):
    city = models.CharField(max_length=50)
    street = models.CharField(max_length=100)
    number = models.PositiveSmallIntegerField()
    name = models.CharField(max_length=100)

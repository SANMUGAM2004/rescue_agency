# models.py
from django.db import models
from base.models import RescueAgency


class Resource(models.Model):
    name = models.CharField(max_length=255)
    quantity = models.IntegerField()
    agency = models.ForeignKey(RescueAgency, on_delete=models.CASCADE)


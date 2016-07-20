from __future__ import unicode_literals

from django.db import models

class Orders(models.Model):
    buy = models.CharField(max_length=25)
    customer = models.CharField(max_length=20)
    email = models.EmailField()
    byn = models.IntegerField(null=True, default=0)
    byr = models.IntegerField(null=True, default=0)
    comment = models.CharField(max_length=50)
    date_create = models.CharField(max_length=10, null=True)
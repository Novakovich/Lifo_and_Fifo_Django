from django.db import models

class Donate(models.Model):
    name = models.CharField(max_length=100)
    amount = models.IntegerField()

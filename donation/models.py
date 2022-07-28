from django.db import models

class Office(models.Model):

    name = models.CharField(max_length=100)


class Donate(models.Model):
    name = models.CharField(max_length=100)
    amount = models.IntegerField()
    state = models.CharField(max_length=100,
        choices=(('Available', 'Available'),
                 ('Requested', 'Requested'),
                 ('Booked', 'Booked'),
                 ('Shipped', 'Shipped')), default='Available'
    )
    office = models.ForeignKey(Office, on_delete=models.CASCADE, null=True)

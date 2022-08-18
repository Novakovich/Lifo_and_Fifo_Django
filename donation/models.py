from django.db import models
from django.db.models import Sum, F


class Office(models.Model):
    name = models.CharField(max_length=100)
    office_count = models.IntegerField(default=0, null=True)
    capacity = models.IntegerField(default=100)

    class Meta:
        constraints = [
            models.CheckConstraint(check=models.Q(office_count__lte=F('capacity')), name='office_count_lte'),
        ]


class Donate(models.Model):
    name = models.CharField(max_length=100)
    amount = models.IntegerField()
    state = models.CharField(max_length=100, choices=(
             ('Available', 'Available'),
             ('Requested', 'Requested'),
             ('Booked', 'Booked'),
             ('Shipped', 'Shipped')), default='Available'
    )
    office = models.ForeignKey(Office, on_delete=models.CASCADE, null=True)


class Request(models.Model):
    request_amount = models.IntegerField(default=0)


class Item(models.Model):
    name_item = models.CharField(max_length=100, default=0)
    amount_item = models.IntegerField(default=0)
    request_hash = models.ForeignKey(Request, on_delete=models.CASCADE, null=True)
    office = models.ForeignKey(Office, on_delete=models.CASCADE, null=True)


def full_storage(sender, instance, **kwargs):
    state = sender.objects.filter(state='Available', office=instance.office_id).aggregate(Sum('amount'))
    instance.office.office_count = state['amount__sum']
    instance.office.save()


models.signals.post_save.connect(receiver=full_storage, sender=Donate)

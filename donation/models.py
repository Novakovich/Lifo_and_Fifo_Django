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


class Request(models.Model):
    request_amount = models.IntegerField(default=0)


class Donate(models.Model):
    donate_amount = models.IntegerField(default=0)


class Item(models.Model):
    name_item = models.CharField(max_length=100, default=0)
    amount_item = models.IntegerField(default=0)
    office = models.ForeignKey(Office, on_delete=models.CASCADE, null=True)

    class Meta:
        abstract = True


class DonateItem(Item):
    state = models.CharField(max_length=100, choices=(
        ('Available', 'Available'),
        ('Booked', 'Booked')), default='Available'
                             )
    request_hash = models.ForeignKey(Donate, on_delete=models.CASCADE, null=True)


class RequestItem(Item):
    state = models.CharField(max_length=100, choices=(
         ('Requested', 'Requested'),
         ('Shipped', 'Shipped')), default='Requested'
                            )
    request_hash = models.ForeignKey(Request, on_delete=models.CASCADE, null=True)


class Description(DonateItem):
    details = models.TextField()


def full_storage(sender, instance, **kwargs):
    state = sender.objects.filter(state='Available', office=instance.office_id).aggregate(Sum('amount_item'))
    instance.office.office_count = state['amount_item__sum']
    instance.office.save()


models.signals.post_save.connect(receiver=full_storage, sender=DonateItem)

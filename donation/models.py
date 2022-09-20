import uuid
from django.db import models
from django.db.models import Sum, F

CONDITION_CHOICES = [
    ('New', 'New'),
    ('Used', 'Used'),
]


class CompleteDonateManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(state='Booked')


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
    datetime = models.DateTimeField(auto_now_add=True)


class Donate(models.Model):
    donate_amount = models.IntegerField(default=0)
    datetime = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True)


class Item(models.Model):
    name_item = models.CharField(max_length=100)
    amount_item = models.IntegerField()
    office = models.ForeignKey(Office, on_delete=models.CASCADE, null=True)

    class Meta:
        abstract = True


class DonateItem(Item):
    state = models.CharField(max_length=100, choices=(
        ('Available', 'Available'),
        ('Booked', 'Booked')), default='Available'
                             )
    donate_uuid = models.ForeignKey(Donate, on_delete=models.CASCADE, db_column='donate_uuid')


class CompleteDonate(DonateItem):
    class Meta:
        proxy = True
    object = CompleteDonateManager()


class RequestItem(Item):
    state = models.CharField(max_length=100, choices=(
         ('Requested', 'Requested'),
         ('Shipped', 'Shipped')), default='Requested'
                            )
    request_hash = models.ForeignKey(Request, on_delete=models.CASCADE, null=True)


class Description(DonateItem):
    details = models.TextField()
    condition = models.CharField(max_length=4, choices=CONDITION_CHOICES, default='New')
    place = models.IntegerField()


def full_storage(sender, instance, **kwargs):
    state = sender.objects.filter(state='Available', office=instance.office_id).aggregate(Sum('amount_item'))
    instance.office.office_count = state['amount_item__sum']
    instance.office.save()


models.signals.post_save.connect(receiver=full_storage, sender=DonateItem)

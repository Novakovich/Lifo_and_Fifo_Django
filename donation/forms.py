from django.forms import formset_factory, Textarea
from .models import Description, Donate
from django import forms


class DescribedItem(forms.ModelForm):

    class Meta:
        model = Description
        exclude = ('request_hash', 'state', 'office')
        widgets = {
            'details': Textarea(attrs={'rows': 10}),
        }

DescribedItemFormSet = formset_factory(DescribedItem)


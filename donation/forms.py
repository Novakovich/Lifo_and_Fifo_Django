from django.forms import ModelForm, Textarea
from .models import Description
from django import forms


class DescribedItem(forms.ModelForm):

    class Meta:
        model = Description
        exclude = ('request_hash', 'state', 'office')
        widgets = {
            'details': Textarea(attrs={'rows': 10}),
        }


from django.forms import formset_factory, Textarea
from .models import Description
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class DescribedItem(forms.ModelForm):
    class Meta:
        model = Description
        exclude = ('donate_uuid', 'state', 'office')
        widgets = {
            'details': Textarea(attrs={'rows': 10}),
        }


DescribedItemFormSet = formset_factory(DescribedItem)


class SearchingItem(forms.ModelForm):
    class Meta:
        model = Description
        fields = ('name_item', 'amount_item', 'condition')


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
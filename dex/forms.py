from django import forms

from dex.models import SellOrder


class OrderForm(forms.ModelForm):
    class Meta:
        model = SellOrder
        fields = ('usr_addr', 'obj', 'value')
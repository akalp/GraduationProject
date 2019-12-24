from django import forms

from dex.models import SellOrder, BuyOrder

class SellOrderForm(forms.ModelForm):
    class Meta:
        model = SellOrder
        fields = ('usr_addr', 'obj', 'value')


class BuyOrderForm(forms.ModelForm):
    class Meta:
        model = BuyOrder
        fields = ('usr_addr', 'obj', 'value')
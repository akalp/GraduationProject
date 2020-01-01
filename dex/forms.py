from django import forms

from dex.models import SellOrder, BuyOrder, Game, Token


class SellOrderForm(forms.ModelForm):
    class Meta:
        model = SellOrder
        fields = ('usr_addr', 'obj', 'value')


class BuyOrderForm(forms.ModelForm):
    class Meta:
        model = BuyOrder
        fields = ('usr_addr', 'obj', 'value')


class GameForm(forms.ModelForm):
    class Meta:
        model = Game
        fields = ('name', 'img', 'desc')


class TokenForm(forms.ModelForm):
    class Meta:
        model = Token
        fields = ('game', 'name', 'img')

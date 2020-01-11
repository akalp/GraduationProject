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
    quantity = forms.IntegerField(initial=1)
    is_nf = forms.TypedChoiceField(label="Token Type", widget=forms.RadioSelect,
                                   choices=((False, 'Fungible'), (True, 'Non-Fungible')), initial=True)
    usr_addr = forms.CharField()

    class Meta:
        model = Token
        fields = ('is_nf', 'game', 'name', 'img')

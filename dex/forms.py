from django import forms
from django.forms import Select

from dex.models import SellOrder, BuyOrder, Game, Token


class CustomSelect(Select):
    def create_option(self, name, value, label, selected, index, subindex=None, attrs=None):
        index = str(index) if subindex is None else "%s_%s" % (index, subindex)
        if attrs is None:
            attrs = {}
        option_attrs = self.build_attrs(self.attrs, attrs) if self.option_inherits_attrs else {}
        if selected:
            option_attrs.update(self.checked_attribute)
        if 'id' in option_attrs:
            option_attrs['id'] = self.id_for_label(option_attrs['id'], index)
        if value != "":
            is_nf = Token.objects.get(pk=value).is_nf
            option_attrs['is_nf'] = str(is_nf)
            if not is_nf:
                option_attrs['contract_id'] = str(Token.objects.get(pk=value).contract_id)
        else:
            option_attrs['is_nf'] = 'True'
        return {
            'name': name,
            'value': value,
            'label': label,
            'selected': selected,
            'index': index,
            'attrs': option_attrs,
            'type': self.input_type,
            'template_name': self.option_template_name,
        }


class SellOrderForm(forms.ModelForm):
    class Meta:
        model = SellOrder
        fields = ('usr_addr', 'obj', 'quantity', 'value')

        widgets = {
            'obj': CustomSelect,
        }


class BuyOrderForm(forms.ModelForm):
    class Meta:
        model = BuyOrder
        fields = ('usr_addr', 'obj', 'quantity', 'value')

        widgets = {
            'obj': CustomSelect,
        }


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

    def __init__(self, user, *args, **kwargs):
        super(TokenForm, self).__init__(*args, **kwargs)
        self.fields['game'].queryset = Game.objects.filter(user=user)

from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views import generic
from dex.models import SellOrder, BuyOrder, Game
from dex.forms import SellOrderForm, BuyOrderForm


class IndexView(generic.TemplateView):
    template_name = 'index.html'


class ListOrder(generic.TemplateView):
    template_name = 'dex/list_orders.html'

    def get_context_data(self, **kwargs):
        game = kwargs.get('game')
        context = super().get_context_data(**kwargs)
        context['games'] = Game.objects.all()
        context['sell_orders'] = SellOrder.objects.filter(obj__game=game if game else Game.objects.first().pk)
        context['buy_orders'] = BuyOrder.objects.filter(obj__game=game if game else Game.objects.first().pk)
        return context


class NewSellOrder(generic.CreateView):
    template_name = 'dex/new_order.html'
    form_class = SellOrderForm
    model = SellOrder

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['title'] = "Satış Emri Ekle"
        data['url'] = reverse('dex:add_sell')
        return data

    def get_success_url(self):
        return reverse_lazy('dex:list_order', kwargs={'game': self.object.obj.game.pk})


class SellDetail(generic.DetailView):
    model = SellOrder
    context_object_name = "order"
    template_name = "dex/detail.html"


class DeleteSellOrder(generic.DeleteView):
    model = SellOrder
    template_name = 'dex/order_delete.html'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['url'] = reverse('dex:delete_sell', kwargs={'pk': self.object.pk})
        return data

    def get_success_url(self):
        return reverse_lazy('dex:list_order', kwargs={'game': self.object.obj.game.pk})


class NewBuyOrder(generic.CreateView):
    template_name = 'dex/new_order.html'
    form_class = BuyOrderForm
    model = BuyOrder

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['title'] = "Alış Emri Ekle"
        data['url'] = reverse('dex:add_buy')
        return data

    def get_success_url(self):
        return reverse_lazy('dex:list_order', kwargs={'game': self.object.obj.game.pk})


class BuyDetail(generic.DetailView):
    model = BuyOrder
    context_object_name = "order"
    template_name = "dex/detail.html"


class DeleteBuyOrder(generic.DeleteView):
    model = BuyOrder
    template_name = 'dex/order_delete.html'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['url'] = reverse('dex:delete_buy', kwargs={'pk': self.object.pk})
        return data

    def get_success_url(self):
        return reverse_lazy('dex:list_order', kwargs={'game': self.object.obj.game.pk})

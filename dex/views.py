from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic
from dex.models import SellOrder, BuyOrder, Game
from dex.forms import SellOrderForm, BuyOrderForm


class IndexView(generic.TemplateView):
    template_name = 'index.html'


class ListOrder(generic.TemplateView):
    template_name = 'dex/list_orders.html'

    def get_context_data(self, **kwargs):
        game = kwargs.get('game')
        print(game)
        context = super().get_context_data(**kwargs)
        context['games'] = Game.objects.all()
        context['sell_orders'] = SellOrder.objects.filter(game=game if game else Game.objects.first().pk)
        context['buy_orders'] = BuyOrder.objects.filter(game=game if game else Game.objects.first().pk)
        return context


class NewSellOrder(generic.CreateView):
    template_name = 'dex/new_order.html'
    form_class = SellOrderForm
    model = SellOrder
    redirect_field_name = "blog/detail.html"


class SellDetail(generic.DetailView):
    model = SellOrder
    context_object_name = "order"
    template_name = "dex/detail.html"


class DeleteSellOrder(generic.DeleteView):
    model = SellOrder
    success_url = reverse_lazy('dex:list_order')


class NewBuyOrder(generic.CreateView):
    template_name = 'dex/new_order.html'
    form_class = BuyOrderForm
    model = BuyOrder
    redirect_field_name = "blog/detail.html"


class BuyDetail(generic.DetailView):
    model = BuyOrder
    context_object_name = "order"
    template_name = "dex/detail.html"


class DeleteBuyOrder(generic.DeleteView):
    model = BuyOrder
    success_url = reverse_lazy('dex:list_order')

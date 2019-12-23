from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic
from dex.models import SellOrder, BuyOrder
from dex.forms import OrderForm
# Create your views here.

class IndexView(generic.TemplateView):
    template_name = 'index.html'


class NewSellOrder(generic.CreateView):
    template_name = 'dex/new_sell.html'
    form_class = OrderForm
    model = SellOrder
    redirect_field_name = "blog/detail.html"


class ListSellOrder(generic.ListView):
    template_name = 'dex/list_orders.html'
    context_object_name = 'orders'

    def get_queryset(self):
        return SellOrder.objects.all()


class SellDetail(generic.DetailView):
    model = SellOrder
    context_object_name = "order"
    template_name = "dex/detail.html"


class DeleteSellOrder(generic.DeleteView):
    model=SellOrder
    success_url = reverse_lazy('dex:list_sell')
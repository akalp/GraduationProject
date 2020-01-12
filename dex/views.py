from django.http import JsonResponse, HttpResponse
from django.shortcuts import redirect
from django.template.loader import render_to_string
from django.urls import reverse_lazy, reverse
from django.views import generic
from .utils import web3_utils

from dex.models import SellOrder, BuyOrder, Game, Token
from dex import forms

from web3 import Web3, HTTPProvider
import json
import os

from GraduationProject.settings import BASE_DIR, web3, erc1155


class IndexView(generic.TemplateView):
    template_name = 'index.html'


class GameListView(generic.ListView):
    modal = Game
    context_object_name = 'games'
    template_name = 'dex/partial/gamelist.html'

    def get_queryset(self):
        return Game.objects.filter(name__istartswith=self.kwargs.get('c'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.GET["from"] == "list_orders":
            context["url"] = reverse("dex:list_order_ajax")
        else:
            context["url"] = reverse("dex:profile")

        return context


class ListOrder(generic.TemplateView):
    template_name = 'dex/list_orders.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        game = kwargs.get('game')
        context["url"] = reverse('dex:list_order_ajax')
        if game:
            context['games'] = Game.objects.filter(name__istartswith=Game.objects.get(pk=game).name[:1])
            context['game'] = game
            context['sell'] = render_to_string('dex/partial/order.html', {
                'orders': SellOrder.objects.filter(obj__game=game).order_by('-timestamp'), 'title': 'Satış Emirleri',
                'button_title': 'Satış Emri Ekle', 'add_url': reverse('dex:add_sell'), 'game': game,
                'detail_url': reverse('dex:detail_sell'), 'delete_url': reverse('dex:delete_sell')})
            context['buy'] = render_to_string('dex/partial/order.html', {
                'orders': BuyOrder.objects.filter(obj__game=game).order_by('-timestamp'), 'title': 'Alış Emirleri',
                'button_title': 'Alış Emri Ekle', 'add_url': reverse('dex:add_buy'),  'game': game,
                'detail_url': reverse('dex:detail_buy'), 'delete_url': reverse('dex:delete_buy')})
        else:
            context['games'] = Game.objects.all()
            context['sell'] = render_to_string('dex/partial/order.html', {
                'orders': SellOrder.objects.all().order_by('-timestamp'), 'title': 'Satış Emirleri',
                'button_title': 'Satış Emri Ekle',
                'detail_url': reverse('dex:detail_sell'), 'delete_url': reverse('dex:delete_sell')})
            context['buy'] = render_to_string('dex/partial/order.html', {
                'orders': BuyOrder.objects.all().order_by('-timestamp'), 'title': 'Alış Emirleri',
                'button_title': 'Alış Emri Ekle',
                'detail_url': reverse('dex:detail_buy'), 'delete_url': reverse('dex:delete_buy')})

        return context


class ListOrderAjax(generic.ListView):
    model = None

    def get(self, request, *args, **kwargs):
        context = {}
        game = kwargs.get('game')
        context['sell'] = render_to_string('dex/partial/order.html', {
            'orders': SellOrder.objects.filter(obj__game=game).order_by('-timestamp'), 'title': 'Satış Emirleri',
            'button_title': 'Satış Emri Ekle', 'add_url': reverse('dex:add_sell'), 'game': game,
            'detail_url': reverse('dex:detail_sell'), 'delete_url': reverse('dex:delete_sell')})
        context['buy'] = render_to_string('dex/partial/order.html', {
            'orders': BuyOrder.objects.filter(obj__game=game).order_by('-timestamp'), 'title': 'Alış Emirleri',
            'button_title': 'Alış Emri Ekle', 'add_url': reverse('dex:add_buy'), 'game': game,
            'detail_url': reverse('dex:detail_buy'), 'delete_url': reverse('dex:delete_buy')})

        return JsonResponse(context)


class NewSellOrder(generic.CreateView):
    template_name = 'dex/new_order.html'
    form_class = forms.SellOrderForm
    model = SellOrder

    def form_invalid(self, form):
        form.fields['obj'].queryset = Token.objects.filter(
            game__name=Game.objects.get(pk=self.request.GET['game']).name)
        data = {
            'result': 'error',
            'message': 'Form invalid',
            'html': render_to_string(self.template_name,
                                     context={'title': 'Satış Emri Ekle', 'game': self.request.GET['game'],
                                              'url': reverse('dex:add_sell'), 'form': form}, request=self.request)
        }
        return JsonResponse(data)

    def form_valid(self, form):
        self.object = form.save()
        data = {
            'result': 'success',
            'message': 'Form valid',
            'url': reverse_lazy('dex:list_order', kwargs={'game': self.object.obj.game.pk})
        }
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)

        ids = web3_utils.getTokenIdsByAddr(self.request.GET['usr_addr'])

        data['from'] = "sell"
        data['game'] = self.request.GET['game']
        data['form'].fields['obj'].queryset = Token.objects.filter(contract_id__in=ids).filter(
            game_id=self.request.GET['game'])
        data['title'] = "Satış Emri Ekle"
        data['url'] = reverse('dex:add_sell')
        return data



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
    form_class = forms.BuyOrderForm
    model = BuyOrder

    def form_invalid(self, form):
        form.fields['obj'].queryset = Token.objects.filter(
            game__name=Game.objects.get(pk=self.request.GET['game']).name)
        data = {
            'result': 'error',
            'message': 'Form invalid',
            'html': render_to_string(self.template_name,
                                     context={'title': 'Alış Emri Ekle', 'game': self.request.GET['game'],
                                              'url': reverse('dex:add_buy'), 'form': form}, request=self.request)
        }
        return JsonResponse(data)

    def form_valid(self, form):
        self.object = form.save()
        data = {
            'result': 'success',
            'message': 'Form valid',
            'url': reverse_lazy('dex:list_order', kwargs={'game': self.object.obj.game.pk})
        }
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['from'] = "buy"
        data['game'] = self.request.GET['game']
        data['form'].fields['obj'].queryset = Token.objects.filter(
            game__name=Game.objects.get(pk=self.request.GET['game']).name)
        data['title'] = "Alış Emri Ekle"
        data['url'] = reverse('dex:add_buy')
        return data


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


class ProfileView(generic.TemplateView):
    template_name = 'dex/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['games'] = Game.objects.all()
        context['url'] = reverse('dex:profile')
        return context


class GameCreateView(generic.CreateView):
    template_name = 'dex/new_game.html'
    form_class = forms.GameForm
    model = Game

    def get_success_url(self):
        return reverse_lazy('dex:list_order', kwargs={'game':self.object.pk})


class TokenCreateView(generic.CreateView):
    template_name = 'dex/new_token.html'
    form_class = forms.TokenForm
    model = Token

    def form_valid(self, form):
        data = form.cleaned_data
        data['game'] = data['game'].id
        id = web3_utils.create_mint(data)
        if id:
            form.instance.contract_id = id
            form.save()
            return redirect(reverse_lazy('dex:list_order'))
        else:
            return HttpResponse('BECEREMEDİM!')

from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.urls import reverse_lazy, reverse
from django.views import generic
from .utils import web3_utils

from dex.models import SellOrder, BuyOrder, Game, Token
from dex import forms


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
            context["url"] = reverse("dex:profile_ajax")

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
                'orders': SellOrder.objects.filter(obj__game=game).order_by('-timestamp'), 'title': 'Sales Orders',
                'button_title': 'Add Sales Order', 'add_url': reverse('dex:add_sell'), 'game': game,
                'detail_url': reverse('dex:detail_sell'), 'delete_url': reverse('dex:delete_sell')})
            context['buy'] = render_to_string('dex/partial/order.html', {
                'orders': BuyOrder.objects.filter(obj__game=game).order_by('-timestamp'), 'title': 'Buy Orders',
                'button_title': 'Add Buy Order', 'add_url': reverse('dex:add_buy'), 'game': game,
                'detail_url': reverse('dex:detail_buy'), 'delete_url': reverse('dex:delete_buy')})
        else:
            context['games'] = Game.objects.all()
            context['sell'] = render_to_string('dex/partial/order.html', {
                'orders': SellOrder.objects.all().order_by('-timestamp'), 'title': 'Sales Orders',
                'button_title': 'Add Sales Order',
                'detail_url': reverse('dex:detail_sell'), 'delete_url': reverse('dex:delete_sell')})
            context['buy'] = render_to_string('dex/partial/order.html', {
                'orders': BuyOrder.objects.all().order_by('-timestamp'), 'title': 'Buy Orders',
                'button_title': 'Add Buy Order',
                'detail_url': reverse('dex:detail_buy'), 'delete_url': reverse('dex:delete_buy')})

        return context


class ListOrderAjax(generic.ListView):
    model = None

    def get(self, request, *args, **kwargs):
        context = {}
        game = kwargs.get('game')
        context['sell'] = render_to_string('dex/partial/order.html', {
            'orders': SellOrder.objects.filter(obj__game=game).order_by('-timestamp'), 'title': 'Sales Orders',
            'button_title': 'Add Sales Order', 'add_url': reverse('dex:add_sell'), 'game': game,
            'detail_url': reverse('dex:detail_sell'), 'delete_url': reverse('dex:delete_sell')})
        context['buy'] = render_to_string('dex/partial/order.html', {
            'orders': BuyOrder.objects.filter(obj__game=game).order_by('-timestamp'), 'title': 'Buy Orders',
            'button_title': 'Add Buy Order', 'add_url': reverse('dex:add_buy'), 'game': game,
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
                                     context={'title': 'Add Sales Order', 'game': self.request.GET['game'],
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
        data['title'] = "Add Sales Order"
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
                                     context={'title': 'Add Buy Order', 'game': self.request.GET['game'],
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
        data['title'] = "Add Buy Order"
        data['url'] = reverse('dex:add_buy')
        return data


class BuyDetail(generic.DetailView):
    model = BuyOrder
    context_object_name = "order"
    template_name = "dex/detail.html"


class DeleteBuyOrder(generic.DeleteView):
    model = BuyOrder
    template_name = 'dex/order_delete.html'

    def post(self, request, *args, **kwargs):
        web3_utils.sendETHtoUser(request.GET.get('usr_addr'), self.get_object().value)
        return super().post(request, *args, **kwargs)

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
        context["url"] = reverse('dex:profile_ajax')
        game = kwargs.get('game')
        usr_addr = self.request.GET.get('usr_addr')
        ids = web3_utils.getTokenIdsByAddr(usr_addr)
        vals = web3_utils.balanceOfBatchSingleAddr(usr_addr, ids)
        zipped = dict(zip(map(str, ids), vals))
        if game:
            context['games'] = Game.objects.filter(name__istartswith=Game.objects.get(pk=game).name[:1])
            context['inventory'] = render_to_string('dex/partial/object.html', {
                'objects': {object: zipped[object.contract_id] for object in
                            Token.objects.filter(game=game, contract_id__in=ids)},
                'game': Game.objects.get(pk=game),
            })
        else:
            context['games'] = Game.objects.all()
            context['inventory'] = render_to_string('dex/partial/object.html', {
                'objects': {object: zipped[object.contract_id] for object in
                            Token.objects.filter(contract_id__in=ids).order_by('-game')},
            })

        return context


class ProfileViewAjax(generic.ListView):
    model = None

    def get(self, request, *args, **kwargs):
        context = {}
        game = kwargs.get('game')
        usr_addr = self.request.GET.get('usr_addr')
        ids = web3_utils.getTokenIdsByAddr(usr_addr)
        vals = web3_utils.balanceOfBatchSingleAddr(usr_addr, ids)
        zipped = dict(zip(map(str, ids), vals))
        context['inventory'] = render_to_string('dex/partial/object.html', {
            'objects': {object: zipped[object.contract_id] for object in
                        Token.objects.filter(game=game, contract_id__in=ids)},
            'game': Game.objects.get(pk=game),
        })
        return JsonResponse(context)


"""
    Authorization
"""


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            next = request.GET.get('next')
            return HttpResponseRedirect(
                next if next else reverse('dex:index'))  ## FIXME redirect me to game developer page
        else:
            return render(request, 'login.html', context={'error': True})
    else:
        return render(request, 'login.html')


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('dex:index'))


def register(request):
    registered = False

    if request.method == 'POST':
        user_form = UserCreationForm(data=request.POST)

        if user_form.is_valid():
            new_user = user_form.save()
            registered = True
        else:
            print(user_form.errors)
    else:
        user_form = UserCreationForm()
    return render(request, 'registration.html', {
        'user_form': user_form,
        'registered': registered
    })


"""
    Game Developer
"""


class GameCreateView(LoginRequiredMixin, generic.CreateView):
    login_url = '/login'
    template_name = 'dex/new_game.html'
    form_class = forms.GameForm
    model = Game

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('dex:list_order', kwargs={'game': self.object.pk})


class TokenCreateView(LoginRequiredMixin, generic.CreateView):
    login_url = '/login'
    template_name = 'dex/new_token.html'
    form_class = forms.TokenForm
    model = Token

    def get(self, request, *args, **kwargs):
        form = self.form_class(request.user)
        return render(request, self.template_name, context={'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.user, request.POST)
        if form.is_valid():
            data = form.cleaned_data
            data['game'] = data['game'].id
            id = web3_utils.create_mint(data)
            if id:
                form.instance.contract_id = id
                form.save()
                return redirect(reverse_lazy('dex:list_order'))
            else:
                return HttpResponse('An error occurred when creating token. Please get contact with administrator.')
        return render(request, self.template_name, context={'form': form})

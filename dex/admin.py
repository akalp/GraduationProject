from django.contrib import admin
from dex.models import SellOrder, BuyOrder, Game, Token

# Register your models here.
admin.site.register(SellOrder)
admin.site.register(BuyOrder)
admin.site.register(Game)
admin.site.register(Token)
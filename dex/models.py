from django.db import models
from django.urls import reverse


class Game(models.Model):
    name = models.CharField(max_length=255)
    img = models.ImageField(upload_to='game', default='game/default_game.png')
    desc = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name


class Token(models.Model):
    name = models.CharField(max_length=255)
    img = models.ImageField(upload_to='token', default='token/default_token.jpg')
    game = models.ForeignKey(Game, on_delete=models.CASCADE)

    def __str__(self):
        return self.game.name + ' - ' + self.name


class Order(models.Model):
    usr_addr = models.CharField(max_length=42)
    obj = models.ForeignKey(Token, on_delete=models.CASCADE)
    value = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)


class SellOrder(Order):
    def get_absolute_url(self):
        return reverse('dex:detail_sell', kwargs={'pk': self.pk})


class BuyOrder(Order):
    def get_absolute_url(self):
        return reverse('dex:detail_buy', kwargs={'pk': self.pk})

from django.db import models
from django.urls import reverse
from datetime import datetime


# TODO add game and token
class Game(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Order(models.Model):
    usr_addr = models.CharField(max_length=42)
    obj = models.CharField(max_length=255)
    value = models.CharField(max_length=255)    # Float ise ether, integer veya karakter ise token
    game = models.ForeignKey(Game, on_delete=models.CASCADE)

class SellOrder(Order):
    def get_absolute_url(self):
        return reverse('dex:detail_sell', kwargs={'pk': self.pk})


class BuyOrder(Order):
    def get_absolute_url(self):
        return reverse('dex:detail_buy', kwargs={'pk': self.pk})



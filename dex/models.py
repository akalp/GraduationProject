from django.db import models
from django.urls import reverse
from datetime import datetime


class Order(models.Model):
    usr_addr = models.CharField(max_length=42)
    obj = models.CharField(max_length=255)
    value = models.CharField(max_length=255)    # Float ise ether, integer veya karakter ise token


class SellOrder(Order):
    def get_absolute_url(self):
        return reverse('dex:detail_sell', kwargs={'pk': self.pk})

    def __str__(self):
        return self.usr_addr+"\t"+self.obj


class BuyOrder(Order):
    pass

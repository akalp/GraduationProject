from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse


class Game(models.Model):
    user = models.ForeignKey(to=get_user_model(), on_delete=models.CASCADE, related_name='games')
    name = models.CharField(max_length=255, unique=True)
    img = models.ImageField(upload_to='game', default='game/default_game.png', verbose_name="Image")
    desc = models.TextField(null=True, blank=True, verbose_name="Description")

    def __str__(self):
        return self.name


def photo_path(instance, filename):
    import os
    from django.template.defaultfilters import slugify
    basefilename, file_extension = os.path.splitext(filename)
    return "token/{}-{}{}".format(slugify(instance.game.name), slugify(instance.name), file_extension)


class Token(models.Model):
    name = models.CharField(max_length=255)
    img = models.ImageField(upload_to=photo_path, default='token/default_token.jpg', verbose_name="Image")
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    is_nf = models.BooleanField(default=True, verbose_name="Is Non-Fungible?")

    contract_id = models.TextField(null=True)

    class Meta:
        unique_together = ('game', 'name',)

    def __str__(self):
        return self.game.name + ' - ' + self.name


class Order(models.Model):
    usr_addr = models.CharField(max_length=42, verbose_name="User ETH Address")
    obj = models.ForeignKey(Token, on_delete=models.CASCADE, verbose_name="Token")
    value = models.CharField(max_length=255, verbose_name="ETH Value")
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name="Created at")
    quantity = models.IntegerField(default=1)


class SellOrder(Order):
    def get_absolute_url(self):
        return reverse('dex:detail_sell', kwargs={'pk': self.pk})


class BuyOrder(Order):
    def get_absolute_url(self):
        return reverse('dex:detail_buy', kwargs={'pk': self.pk})

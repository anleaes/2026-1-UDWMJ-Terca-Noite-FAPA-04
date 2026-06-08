from django.db import models
from item.models import Item
from auction.models import Auction

# Create your models here.

class AuctionItem(models.Model):
    quantity = models.IntegerField('Quantidade',null=True, blank=True,default=0)
    value = models.FloatField('Preco unitario',null=True, blank=True, default=0.0)
    sub_total = models.FloatField('Preco unitario',null=True, blank=True, default=0.0)
    auction = models.ForeignKey('auction.Auction', on_delete=models.CASCADE, related_name='auction_items')
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='items')


    class Meta:
        verbose_name = 'Item de leilao'
        verbose_name_plural = 'Itens de leilao'
        ordering =['id']

    def __str__(self):
        return "%s" % (self.id)
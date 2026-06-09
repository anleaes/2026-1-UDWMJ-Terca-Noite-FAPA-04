from django.db import models
from auctioneer.models import Auctioneer
from item.models import Item


class Auction(models.Model):
    title = models.CharField('Titulo', max_length=50)
    description = models.TextField('Descricao', max_length=100)
    date_begin = models.DateTimeField('Data de Inicio')
    date_end = models.DateTimeField('Data de Fim')
    initial_value = models.FloatField('Preco Inicial', null=True, blank=True, default=0.0)
    auctioneer = models.ForeignKey(Auctioneer, on_delete=models.CASCADE)
    status = models.CharField('Status', max_length=20, null=True, blank=True, default='Em andamento',choices=[
        ('Em andamento', 'Em andamento'),
        ('Finalizado', 'Finalizado'),
        ('Cancelado', 'Cancelado'),
    ])

    class Meta:
        verbose_name = 'Leilao'
        verbose_name_plural = 'Leiloes'
        ordering =['id']

    def __str__(self):
        return "%s" % (self.id)
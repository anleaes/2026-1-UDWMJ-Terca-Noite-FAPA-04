from django.db import models
from user.models import User
from auctioneer.models import Auctioneer


class Auction(models.Model):
    title = models.CharField('Titulo', max_length=50)
    description = models.TextField('Descricao', max_length=100)
    date_begin = models.DateTimeField('Data de Inicio')
    date_end = models.DateTimeField('Data de Fim')
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField('Status', max_length=20, null=True, blank=True, default='Em andamento',choices=[
        ('Em andamento', 'Em andamento'),
        ('Finalizado', 'Finalizado'),
        ('Cancelado', 'Cancelado'),
    ])
    initial_value = models.FloatField('Preco Inicial', null=True, blank=True, default=0.0)
    auctioneer = models.ForeignKey(Auctioneer, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Leilao'
        verbose_name_plural = 'Leiloes'
        ordering =['id']

    def __str__(self):
        return "%s" % (self.id)

    @property
    def payment_method(self):
        if hasattr(self, 'payment'):
            return self.payment.payment_method
        return None

    def get_payment_method_display(self):
        if hasattr(self, 'payment'):
            return self.payment.get_payment_method_display()
        return None

    @property
    def user(self):
        if hasattr(self, 'payment'):
            return self.payment.user
        return None

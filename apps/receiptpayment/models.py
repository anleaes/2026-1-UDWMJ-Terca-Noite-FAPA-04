from django.db import models
from auction.models import Auction
from payment.models import Payment

class Receipt(models.Model):
    number = models.CharField('Número', max_length=100, unique=True)
    issue_date = models.DateField('Data de emissão', auto_now_add=True)
    auction = models.OneToOneField(Auction, on_delete=models.CASCADE)
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        verbose_name = 'Recibo'
        verbose_name_plural = 'Recibos'
        ordering = ['id']

    def __str__(self):
        return self.number

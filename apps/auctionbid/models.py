from django.db import models


class AuctionBid(models.Model):
    STATUS_CHOICES = [
        ('P', 'Pendente'),
        ('A', 'Aceito'),
        ('R', 'Recusado'),
    ]

    value = models.DecimalField('Valor', max_digits=10, decimal_places=2)
    status = models.CharField('Status', max_length=1, choices=STATUS_CHOICES, default='P')
    user = models.ForeignKey('user.User', on_delete=models.CASCADE, related_name='auction_bids')
    auction = models.ForeignKey('auction.Auction', on_delete=models.CASCADE, related_name='bids')
    auctionitem = models.ForeignKey('auctionitem.AuctionItem', on_delete=models.CASCADE, related_name='auction_bids')

    class Meta:
        verbose_name = 'Lance'
        verbose_name_plural = 'Lances'
        ordering = ['id']

    def __str__(self):
        return f'Lance {self.id} - {self.user} - {self.value}'

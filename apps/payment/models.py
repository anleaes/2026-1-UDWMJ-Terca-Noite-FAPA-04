from django.db import models
from auction.models import Auction
from user.models import User


PAYMENT_METHOD_CHOICES = [
    ('C', 'Cartão de Crédito'),
    ('D', 'Débito'),
    ('P', 'Pix'),
    ('B', 'Boleto'),
]


class Payment(models.Model):
    total = models.DecimalField('Valor total', max_digits=10, decimal_places=2)
    date_payment = models.DateField('Data do pagamento', auto_now_add=True)
    payment_method = models.CharField('Método de pagamento', max_length=50, choices=PAYMENT_METHOD_CHOICES)
    status = models.CharField('Status do pagamento', max_length=20, choices=[
        ('P', 'Pendente'),
        ('C', 'Concluído'),
        ('F', 'Falhado'),
    ])
    auction = models.OneToOneField(Auction, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Pagamento'
        verbose_name_plural = 'Pagamentos'
        ordering = ['id']

    def __str__(self):
        return f'Pagamento {self.id}'
        

class PaymentMethod(models.Model):
    name = models.CharField('Nome', max_length=80)
    method = models.CharField('Tipo', max_length=1, choices=PAYMENT_METHOD_CHOICES)
    description = models.CharField('Descrição', max_length=120, blank=True)
    is_active = models.BooleanField('Ativo', default=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='payment_methods')

    class Meta:
        verbose_name = 'Método de pagamento'
        verbose_name_plural = 'Métodos de pagamento'
        ordering = ['id']

    def __str__(self):
        return self.name

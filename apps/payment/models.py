from django.db import models

class Payment(models.Model):

    name = models.CharField(
        'Nome do pagamento',
        max_length=100, null=False, blank=False
    )

    description = models.TextField(
        'Descrição do pagamento',
        blank=True,
        null=True
    )

    is_active = models.BooleanField(
        'Ativo',
        default=True
    )

    payment_method = models.CharField(
        'Método de pagamento',
        max_length=50,
        choices=[
            ('C', 'Cartão de Crédito'),
            ('D', 'Débito'),
            ('P', 'Pix'),
            ('B', 'Boleto'),
        ]
    )

    class Meta:
        verbose_name = 'Método de Pagamento'
        verbose_name_plural = 'Métodos de Pagamento'

    def __str__(self):
        return self.name
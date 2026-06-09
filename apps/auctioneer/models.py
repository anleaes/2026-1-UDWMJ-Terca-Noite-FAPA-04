from django.db import models
from person.models import Person
from contactchannel.models import Contactchannel

class Auctioneer(Person):
    company = models.CharField('Empresa', max_length=100)
    evaluation = models.FloatField('Avaliacao',null=True, blank=True, default=0.0)
    commission = models.FloatField('Comissao',null=True, blank=True, default=0.0)
    status = models.BooleanField('Status', default=True)
    contactchannel = models.ForeignKey(Contactchannel, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        verbose_name = 'Leiloeiro'
        verbose_name_plural = 'Leiloeiros'
        ordering =['id']

    def __str__(self):
        return super().first_name

from django.db import models
from person.models import Person
from contactchannel.models import Contactchannel

class User(Person):
    balance = models.FloatField('Saldo', null=True, blank=True, default=0.0)
    reputation = models.FloatField('Reputação', null=True, blank=True, default=0.0)
    gender = models.CharField('Genero', max_length=1, choices=[
        ('M', 'Masculino'),
        ('F', 'Feminino'),
        ('O', 'Outro'),
    ])
    contactchannel = models.ManyToManyField(Contactchannel, verbose_name="Canais de Contato")
    
    class Meta:
        verbose_name = 'Usuário'
        verbose_name_plural = 'Usuários'
        ordering =['id']

    def __str__(self):
        return super().first_name

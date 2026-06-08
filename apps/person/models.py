from django.db import models
from contactchannel.models import Contactchannel


class Person(models.Model):
    first_name = models.CharField('Nome', max_length=50)
    last_name = models.CharField('Sobrenome', max_length=100) 
    email = models.EmailField('E-mail',null=False, blank=False)
    password = models.CharField('Senha', max_length=128)
    
    class Meta:
        verbose_name = 'Pessoa'
        verbose_name_plural = 'Pessoas'
        ordering =['id']

    def __str__(self):
        return self.first_name
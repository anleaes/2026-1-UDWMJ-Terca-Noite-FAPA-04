from django.db import models

# Create your models here.

class Contactchannel(models.Model):
    name = models.CharField('Nome', max_length=50)
    content_type = models.TextField('Tipo de conteúdo', max_length=100) 
    url = models.CharField('URL do Canal de Contato', max_length=200)
    
    class Meta:
        verbose_name = 'Canal de Contato'
        verbose_name_plural = 'Canais de Contato'
        ordering =['id']

    def __str__(self):
        return self.name
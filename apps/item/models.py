from django.db import models
from category.models import Category

class Item(models.Model):
    name = models.CharField('Nome', max_length=50)
    description = models.TextField('Descricao', max_length=100)
    fabrication_date = models.DateField('Data Fabricacao', auto_now=False, auto_now_add=False) 
    price = models.DecimalField('Preço', max_digits=10, decimal_places=2, default=0)
    photo = models.ImageField('Foto', upload_to='photos')
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    
    class Meta:
        verbose_name = 'Item'
        verbose_name_plural = 'Itens'
        ordering =['id']

    def __str__(self):
        return self.name
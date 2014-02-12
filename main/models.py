from django.db import models

class Product(models.Model):
    '''
    Class to define the Product model
    '''
    def __unicode__(self):
        return self.name

    name = models.CharField(max_length=100, verbose_name='Nombre')
    price = models.FloatField(verbose_name='Precio')
    active = models.BooleanField(default=True)
from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

class Product(models.Model):
    '''
    Class to define the Product model
    '''
    def __unicode__(self):
        return self.model

    model = models.CharField(max_length=100, verbose_name='Nombre')
    price = models.FloatField(verbose_name='Precio')
    active = models.BooleanField(default=True)
    photo = models.FileField(
        upload_to='main/static/media/photos',
        verbose_name="Foto",
    )

class CategorySample(models.Model):
    '''
    Class to define the Product sample model
    '''
    def __unicode__(self):
        return self.name

    name = models.CharField(max_length=100, verbose_name='Nombre')
    active = models.BooleanField(default=True)


class ProductSample(models.Model):
    '''
    Class to define the Product sample model
    '''
    def __unicode__(self):
        return self.name

    name = models.CharField(max_length=100, verbose_name='Nombre')
    active = models.BooleanField(default=True)
    category = models.ForeignKey(CategorySample, related_name='products_sample', verbose_name="Categoria")
    photo = models.FileField(
        upload_to='main/static/media/photos',
        verbose_name="Foto",
    )

class Order(models.Model):
    '''
    Class to define the Order model
    '''
    def __unicode__(self):
        return self.product.model

    product = models.ForeignKey(Product, related_name='orders', verbose_name="product")
    client = models.ForeignKey(User, related_name='orders', verbose_name="client")
    color = models.CharField(
        max_length=50,
        choices=settings.COLORS,
        verbose_name="Color"
    )
    size = models.CharField(
        max_length=2,
        choices=settings.SIZES,
        verbose_name="Talla"
    )
    quantity = models.CharField(max_length=10, verbose_name="Cantidad")

class SiteConfiguration(models.Model):
    '''
    Class to define configurations
    '''
    background = models.FileField(
        upload_to='main/static/media/photos',
        verbose_name="Fondo de sitio",
        null=True,
        blank=True,
    )
    active_background = models.BooleanField(default=False, verbose_name="Activar fondo")
    email_to_notifications = models.EmailField(verbose_name="Correo de notificaciones", null=True, blank=True)
from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

class Category(models.Model):
    '''
    Class to define the Product sample model
    '''
    def __unicode__(self):
        return self.name

    name = models.CharField(max_length=100, verbose_name=_('Nombre'))
    active = models.BooleanField(default=True)
    photo = models.FileField(
        upload_to='main/static/media/photos',
        verbose_name="Foto",
    )

class Product(models.Model):
    '''
    Class to define the Product model
    '''
    def __unicode__(self):
        return self.model

    model = models.CharField(max_length=100, verbose_name=_('Nombre'))
    description = models.TextField(max_length=500, verbose_name=_('Descripcion'))
    price = models.FloatField(verbose_name=_('Precio'))
    active = models.BooleanField(default=True)
    photo = models.FileField(
        upload_to='main/static/media/photos',
        verbose_name="Foto",
    )
    category = models.ForeignKey(Category, related_name='products', verbose_name=_("Categoria"))


class ImageSlider(models.Model):
    '''
    Class to define the Product model
    '''
    def __unicode__(self):
        return self.model
    CATEGORY_CHOICES = (
        ('1', 'Slider principal'),
        ('2', 'Slider productos'),
    )
    name = models.CharField(max_length=100, verbose_name=_('Nombre'))
    active = models.BooleanField(default=True)
    photo = models.FileField(
        upload_to='main/static/media/photos',
        verbose_name="Foto",
    )
    category = models.CharField(max_length=1, verbose_name=_('Categoria'), choices=CATEGORY_CHOICES, default='1')

class CategorySample(models.Model):
    '''
    Class to define the Product sample model
    '''
    def __unicode__(self):
        return self.name

    name = models.CharField(max_length=100, verbose_name=_('Nombre'))
    active = models.BooleanField(default=True)


class ProductSample(models.Model):
    '''
    Class to define the Product sample model
    '''
    def __unicode__(self):
        return self.name

    name = models.CharField(max_length=100, verbose_name=_('Nombre'))
    active = models.BooleanField(default=True)
    category = models.ForeignKey(CategorySample, related_name='products_sample', verbose_name=_("Categoria"))
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

    product = models.ForeignKey(Product, related_name='orders', verbose_name=_("product"))
    client = models.ForeignKey(User, related_name='orders', verbose_name=_("client"))
    qty_1= models.IntegerField(verbose_name="1", null=True, blank=True)
    qty_2= models.IntegerField(verbose_name="2", null=True, blank=True)
    qty_3= models.IntegerField(verbose_name="3", null=True, blank=True)
    qty_4= models.IntegerField(verbose_name="4", null=True, blank=True)
    qty_6= models.IntegerField(verbose_name="6", null=True, blank=True)
    qty_8= models.IntegerField(verbose_name="8", null=True, blank=True)
    qty_10= models.IntegerField(verbose_name="10", null=True, blank=True)
    qty_12= models.IntegerField(verbose_name="12", null=True, blank=True)
    qty_14= models.IntegerField(verbose_name="14", null=True, blank=True)
    qty_16= models.IntegerField(verbose_name="16", null=True, blank=True)
    color = models.CharField(
        max_length=50,
        choices=settings.COLORS,
        verbose_name="Color"
    )

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
    active_background = models.BooleanField(default=False, verbose_name=_("Activar fondo"))
    email_to_notifications = models.EmailField(verbose_name=_("Correo de notificaciones"), null=True, blank=True)

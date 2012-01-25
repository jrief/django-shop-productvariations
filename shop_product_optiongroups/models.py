# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _
from django.db import models
from shop.util.fields import CurrencyField


#===============================================================================
# Multiple choice options
#===============================================================================

class OptionGroup(models.Model):
    '''
    A logical group of options
    Example: "Colors"
    '''
    name = models.CharField(max_length=255)
    slug = models.SlugField() # Used in forms for example
    description = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        verbose_name = _('Option Group')
        verbose_name_plural = _('Option Groups')
        db_table = 'shop_product_option_groups'

    def __unicode__(self):
        return self.name

    def get_options(self):
        '''
        A helper method to retrieve a list of options in this OptionGroup
        '''
        options = Option.objects.filter(group=self)
        return options


class Option(models.Model):
    '''
    A product option. Example: Red, 10.0; Green: 20.0; Blue, 30.0;
    '''
    name = models.CharField(max_length=255)
    price = CurrencyField() # Can be negative
    group = models.ForeignKey(OptionGroup)

    class Meta:
        verbose_name = _('Group Option')
        verbose_name_plural = _('Group Options')
        db_table = 'shop_product_options'

    def __unicode__(self):
        return self.name


class ProductOptionGroupsMixin(models.Model):
    """
    A mixin for product definitions with grouped options
    """
    class Meta(object):
        abstract = True
        verbose_name = _('Product mixin with options from named groups')

    options_groups = models.ManyToManyField(OptionGroup, blank=True, null=True)

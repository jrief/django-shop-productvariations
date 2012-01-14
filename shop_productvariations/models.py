# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _
from django.db import models
from shop.models.productmodel import Product
from shop.util.fields import CurrencyField


#===============================================================================
# Text options
#===============================================================================

class TextOption(models.Model):
    """
    This part of the option is selected by the merchant - it lets him/her "flag"
    a product as being able to receive some text as an option, and sets its
    price.
    """
    name = models.CharField(max_length=255, help_text="A name for this option - this will be displayed to the user")
    description = models.CharField(max_length=255, null=True, blank=True, help_text='A longer description for this option')
    price = CurrencyField(help_text='Price per character for this custom text')
    max_length = models.IntegerField()
    
    class Meta:
        verbose_name = _('Text Option')
        verbose_name_plural = _('Text Options')

    def __unicode__(self):
        return self.name

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

    def __unicode__(self):
        return self.name


#===============================================================================
# A product definition with variable options
#===============================================================================

class VariableProduct(Product):
    """
    A product definition with variable options
    """
    class Meta(object):
        abstract = True
        verbose_name = _('Variable product')
        verbose_name_plural = _('Variable products')

    text_options = models.ManyToManyField(TextOption, blank=True, null=True)
    options_groups = models.ManyToManyField(OptionGroup, blank=True, null=True)

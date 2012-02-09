# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.db import models
from shop.util.fields import CurrencyField
from shop.util.loader import get_model_string


#===============================================================================
# Multiple choice options
#===============================================================================

class OptionGroupBase(models.Model):
    '''
    A logical group of options
    Example: "Colors"
    '''
    name = models.CharField(max_length=255)
    slug = models.SlugField() # Used in forms for example
    description = models.CharField(max_length=255, blank=True, null=True)

    class Meta(object):
        abstract = True
        verbose_name = _('Option Group')
        verbose_name_plural = _('Option Groups')
#        db_table = 'shop_product_option_groups'

    def __unicode__(self):
        return self.name

    def get_options(self):
        '''
        A helper method to retrieve a list of options in this OptionGroup
        '''
        options = get_model_string('Option').objects.filter(group=self)
        return options


class OptionBase(models.Model):
    '''
    A product option. Example: Red, 10.0; Green: 20.0; Blue, 30.0;
    '''
    name = models.CharField(max_length=255)
    price = CurrencyField() # Can be negative
    group = models.ForeignKey(get_model_string('OptionGroup'))

    class Meta(object):
        abstract = True
        verbose_name = _('Group Option')
        verbose_name_plural = _('Group Options')
#        db_table = 'shop_product_options'

    def __unicode__(self):
        return self.name
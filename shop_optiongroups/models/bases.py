# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _
from django.db import models
from shop.util.fields import CurrencyField
from shop.util.loader import get_model_string


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

    def __unicode__(self):
        return self.name

    def get_options(self):
        '''
        A helper method to retrieve a list of options in this OptionGroup
        '''
        options = get_model_string('Option', namespace='shop_optiongroups').objects.filter(group=self)
        return options


class OptionBase(models.Model):
    '''
    A product option. Example: Red, 10.0; Green: 20.0; Blue, 30.0;
    '''
    name = models.CharField(max_length=255)
    price = CurrencyField() # Can be negative
    group = models.ForeignKey(get_model_string('OptionGroup', namespace='shop_optiongroups'))

    class Meta(object):
        abstract = True
        verbose_name = _('Group Option')
        verbose_name_plural = _('Group Options')

    def __unicode__(self):
        return self.name

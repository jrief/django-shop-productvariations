# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.db import models
from shop.util.loader import load_class
from bases import OptionGroupBase, OptionBase

#===============================================================================
# Multiple choice options
#===============================================================================

class OptionGroup(OptionGroupBase):
    class Meta(object):
        abstract = False
        app_label = 'shop'


class Option(OptionBase):
    class Meta(object):
        abstract = False
        app_label = 'shop'


VARIATION_OPTIONGROUP_MODEL = getattr(settings, 'VARIATION_OPTIONGROUP_MODEL',
    'shop_product_optiongroups.models.OptionGroup')
OptionGroup = load_class(VARIATION_OPTIONGROUP_MODEL, 'VARIATION_OPTIONGROUP_MODEL')


VARIATION_OPTION_MODEL = getattr(settings, 'VARIATION_OPTION_MODEL',
    'shop_product_optiongroups.models.Option')
Option = load_class(VARIATION_OPTION_MODEL, 'VARIATION_OPTION_MODEL')


class ProductOptionGroupsMixin(models.Model):
    """
    A mixin for product definitions with grouped options
    """
    class Meta(object):
        abstract = True
        verbose_name = _('Product mixin with options from named groups')

    options_groups = models.ManyToManyField(OptionGroup, blank=True, null=True)

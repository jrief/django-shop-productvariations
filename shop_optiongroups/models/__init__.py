# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.db import models
from shop.util.loader import load_class, get_model_string
from bases import OptionGroupBase, OptionBase

#===============================================================================
# Multiple choice options
#===============================================================================

class OptionGroup(OptionGroupBase):
    class Meta(object):
        abstract = False
        app_label = 'shop_optiongroups'


class Option(OptionBase):
    class Meta(object):
        abstract = False
        app_label = 'shop_optiongroups'

OPTIONGROUP_MODEL = getattr(settings, 'SHOP_OPTIONGROUP_MODEL',
    'shop_optiongroups.models.OptionGroup')
OptionGroup = load_class(OPTIONGROUP_MODEL, 'SHOP_OPTIONGROUP_MODEL')


OPTION_MODEL = getattr(settings, 'SHOP_OPTION_MODEL',
    'shop_optiongroups.models.Option')
Option = load_class(OPTION_MODEL, 'SHOP_OPTION_MODEL')


class ProductOptionGroupsMixin(models.Model):
    """
    A mixin for product definitions with grouped options
    """
    class Meta(object):
        abstract = True
        verbose_name = _('Product mixin with options from named groups')

    options_groups = models.ManyToManyField(OptionGroup, blank=True, null=True)

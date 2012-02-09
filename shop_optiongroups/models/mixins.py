# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _
from django.db import models
from shop.util.loader import get_model_string


class ProductOptionGroupsMixin(models.Model):
    """
    A mixin for product definitions with grouped options
    """
    class Meta(object):
        abstract = True
        verbose_name = _('Product mixin with options from named groups')

    options_groups = models.ManyToManyField(get_model_string('OptionGroup', namespace='shop_optiongroups'),
                                            blank=True, null=True)

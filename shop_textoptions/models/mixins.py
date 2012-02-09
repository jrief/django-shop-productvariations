# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _
from django.db import models
from shop.util.loader import get_model_string


class ProductTextOptionsMixin(models.Model):
    """
    A mixin for product definitions with text options
    """
    class Meta(object):
        abstract = True
        verbose_name = _('Product mixin with customizable text options')

    text_options = models.ManyToManyField(get_model_string('TextOption', 'shop_textoptions'),
                                          blank=True, null=True)

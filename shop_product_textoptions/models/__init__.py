# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.db import models
from shop.util.loader import load_class
from bases import TextOptionBase


class TextOption(TextOptionBase):
    class Meta:
        abstract = False
        app_label = 'shop'

    def __unicode__(self):
        return self.name


VARIATION_TEXTOPTION_MODEL = getattr(settings, 'VARIATION_TEXTOPTION_MODEL',
    'shop_product_textoptions.models.TextOptions')
TextOptions = load_class(VARIATION_TEXTOPTION_MODEL, 'VARIATION_TEXTOPTION_MODEL')


class ProductTextOptionsMixin(models.Model):
    """
    A mixin for product definitions with text options
    """
    class Meta(object):
        abstract = True
        verbose_name = _('Product mixin with customizable text options')

    text_options = models.ManyToManyField(TextOption, blank=True, null=True)

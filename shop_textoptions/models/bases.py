# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _
from django.db import models
from shop.util.fields import CurrencyField


class TextOptionBase(models.Model):
    """
    This part of the option is selected by the merchant - it lets him/her "flag"
    a product as being able to receive some text as an option, and sets its
    price.
    """
    name = models.CharField(max_length=255,
        help_text=_('A name for this option - this will be displayed to the user'))
    description = models.CharField(max_length=255, null=True, blank=True,
        help_text=_('A longer description for this option'))
    price = CurrencyField(help_text=_('Price per character for this custom text'))
    max_length = models.IntegerField()
    
    class Meta(object):
        abstract = True
        verbose_name = _('Text Option')
        verbose_name_plural = _('Text Options')

    def __unicode__(self):
        return self.name



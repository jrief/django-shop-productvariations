# -*- coding: utf-8 -*-
from bases import TextOptionBase


class TextOption(TextOptionBase):
    class Meta:
        abstract = False
        app_label = 'shop_textoptions'

    def __unicode__(self):
        return self.name

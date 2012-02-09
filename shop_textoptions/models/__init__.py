# -*- coding: utf-8 -*-
from django.conf import settings
from shop.util.loader import load_class


TEXTOPTION_MODEL = getattr(settings, 'SHOP_TEXTOPTION_MODEL',
    'shop_textoptions.models.defaults.TextOption')
TextOption = load_class(TEXTOPTION_MODEL, 'SHOP_TEXTOPTION_MODEL')


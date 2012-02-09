# -*- coding: utf-8 -*-
from django.conf import settings
from shop.util.loader import load_class


OPTIONGROUP_MODEL = getattr(settings, 'SHOP_OPTIONGROUP_MODEL',
    'shop_optiongroups.models.defaults.OptionGroup')
OptionGroup = load_class(OPTIONGROUP_MODEL, 'SHOP_OPTIONGROUP_MODEL')


OPTION_MODEL = getattr(settings, 'SHOP_OPTION_MODEL',
    'shop_optiongroups.models.defaults.Option')
Option = load_class(OPTION_MODEL, 'SHOP_OPTION_MODEL')

# -*- coding: utf-8 -*-
from bases import OptionGroupBase, OptionBase


class OptionGroup(OptionGroupBase):
    class Meta(object):
        abstract = False
        app_label = 'shop_optiongroups'


class Option(OptionBase):
    class Meta(object):
        abstract = False
        app_label = 'shop_optiongroups'

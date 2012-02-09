# -*- coding: utf-8 -*-
from django.db import models
from shop.models.productmodel import Product
from shop_optiongroups.models.mixins import ProductOptionGroupsMixin
from shop_textoptions.models.mixins import ProductTextOptionsMixin


class DiaryProduct(Product, ProductOptionGroupsMixin, ProductTextOptionsMixin):
    isbn = models.CharField(max_length=255)
    number_of_pages = models.IntegerField()


class CalendarProduct(Product, ProductOptionGroupsMixin):
    isbn = models.CharField(max_length=255)
    number_of_pages = models.IntegerField()

# -*- coding: utf-8 -*-
from django.shortcuts import redirect
from shop_productvariations.views import VariableProductDetail
from models import DiaryProduct


class DiaryDetailView(VariableProductDetail):
    """
    This view handles displaying the detail view for test product Diary 
    """
    model = DiaryProduct

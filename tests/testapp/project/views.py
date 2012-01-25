# -*- coding: utf-8 -*-
from shop.views.product import ProductDetailView
from shop.util.cart import get_or_create_cart
from shop_product_optiongroups.views import ProductOptionGroupsViewMixin
from shop_product_textoptions.views import ProductTextOptionsViewMixin
from models import DiaryProduct, CalendarProduct


class DiaryDetailView(ProductOptionGroupsViewMixin, \
                      ProductTextOptionsViewMixin, ProductDetailView):
    """
    This view handles displaying the detail view for test product Diary 
    """
    model = DiaryProduct

    def post(self, *args, **kwargs):
        super(DiaryDetailView, self).post(*args, **kwargs)
        if self.request.POST['product_action'] == 'add_to_cart':
            self.add_to_cart()

    def add_to_cart(self):
        product = self.get_object()
        variation = self.get_variation(product)
        product_quantity = self.request.POST.get('add_item_quantity')
        if not product_quantity:
            product_quantity = 1
        cart = get_or_create_cart(self.request)
        cart.add_product(product, product_quantity, variation)
        cart.save()

class CalendarDetailView(ProductOptionGroupsViewMixin, ProductDetailView):
    """
    This view handles displaying the detail view for test product Diary 
    """
    model = CalendarProduct

    def post(self, *args, **kwargs):
        super(CalendarDetailView, self).post(*args, **kwargs)
        if self.request.POST['product_action'] == 'add_to_cart':
            self.add_to_cart()

    def add_to_cart(self):
        product = self.get_object()
        variation = self.get_variation(product)
        product_quantity = self.request.POST.get('add_item_quantity')
        if not product_quantity:
            product_quantity = 1
        cart = get_or_create_cart(self.request)
        cart.add_product(product, product_quantity, variation)
        cart.save()

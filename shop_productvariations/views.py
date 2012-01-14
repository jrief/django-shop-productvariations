# -*- coding: utf-8 -*-
from shop.util.cart import get_or_create_cart
from models import VariableProduct, Option


class ProductDetailViewMixin(object):
    """
    Mixin detail view when using ProductVariations
    """
    def post(self, *args, **kwargs):
        super(ProductDetailViewMixin, self).post(*args, **kwargs)
        if self.request.POST['product_action'] == 'add_to_cart':
            self.add_to_cart()

    def add_to_cart(self):
        product = self.get_object()
        if hasattr(self, 'get_variation') and callable(self.get_variation):
            variation = self.get_variation(product)
        else:
            variation = None
        product_quantity = self.request.POST.get('add_item_quantity')
        if not product_quantity:
            product_quantity = 1
        cart = get_or_create_cart(self.request)
        cart.add_product(product, product_quantity, variation)
        cart.save()
    
    def get_variation(self, product):
        """
        The post request contains information about the chosen variation.
        Recombine this with the information extracted from the OptionGroup
        for the given product
        """
        variation = { 
            'text_options': {},
            'option_groups': {},
        }
        for option_group in product.options_groups.all():
            key = 'add_item_option_group_%s' % option_group.id
            if self.request.POST.has_key(key):
                key = int(self.request.POST[key])
                value = option_group.__dict__
                del value['_state']
                value['option'] = Option.objects.get(pk=key).__dict__
                del value['option']['_state']
                variation['option_groups'][option_group.id] = value
        for text_option in product.text_options.all():
            key = 'add_item_text_option_%s' % text_option.id
            if self.request.POST.has_key(key):
                value = text_option.__dict__
                del value['_state']
                value['text'] = self.request.POST[key]
                variation['text_options'][text_option.id] = value
        return variation

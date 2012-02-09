#-*- coding: utf-8 -*-
from decimal import Decimal
from shop.cart.cart_modifiers_base import BaseCartModifier


class TextOptionsOptionsCartModifier(BaseCartModifier):
    '''
    This modifier adds an extra field to the cart to let the lineitem "know"
    about product options and their respective price.
    '''
    def process_cart_item(self, cart_item, state):
        '''
        This adds a list of price modifiers depending on the product options
        the client selected for the current cart_item (if any)
        '''
        # process text_options as passed through the variation object
        if cart_item.variation.has_key('text_options'):
            for value in cart_item.variation['text_options'].itervalues():
                label = value['name'] + ': ' + value['text']
                price = Decimal(value['price']) * len(value['text']) * cart_item.quantity
                # Don't forget to update the running total!
                cart_item.current_total += price
                cart_item.extra_price_fields.append((label, price))
        return cart_item

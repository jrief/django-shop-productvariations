from django import template
from decimal import Decimal


register = template.Library()

@register.filter
def get_option_groups(product):
    """Returns all option groups for the given product."""
    return product.options_groups.all()

@register.filter
def get_options(product):
    """Returns all options for the given option group."""
    return product.option_set.all()

@register.simple_tag
def describe_textoptions(variation):
    '''
    From the given variation object, build a variations description to be used 
    in simple text fields.
    '''
    # process text_options as passed through the variation object
    labels = []
    if variation.has_key('text_options'):
        for value in variation['text_options'].itervalues():
            if len(value['text'])>0:
                labels.append(value['name'] + ': ' + value['text'])
    return '; '.join(labels)

@register.filter
def adjust_textoptions_price(price, variation):
    '''
    From the given variation object, adjust the price to be displayed. 
    '''
    if variation.has_key('text_options'):
        for value in variation['text_options'].itervalues():
            price += Decimal(value['price']) * len(value['text'])
    return price

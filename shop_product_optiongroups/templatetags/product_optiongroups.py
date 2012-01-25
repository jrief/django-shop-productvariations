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

@register.filter
def describe_optiongroups(label=None, variation):
    '''
    From the given variation object, build a variations description to be used 
    in simple text fields.
    '''
    # process option_groups as passed through the variation object
    labels = []
    if variation.has_key('option_groups'):
        for value in variation['option_groups'].itervalues():
            labels.append(value['name'] + ': ' + value['option']['name'])
    if label is not None:
        label += '. '
    return label + '; '.join(labels)

@register.filter
def adjust_optiongroups_price(price, variation):
    '''
    From the given variation object, adjust the price to be displayed. 
    '''
    if variation.has_key('option_groups'):
        for value in variation['option_groups'].itervalues():
            price += Decimal(value['option']['price'])
    return price

# -*- coding: utf-8 -*-
from models import Option


class ProductOptionGroupsViewMixin(object):
    """
    DetailView Mixin class when using ProductOptionGroupsMixin
    """

    def get_variation(self):
        """
        The post request contains information about the chosen variation.
        Recombine this with the information extracted from the OptionGroup
        for the given product
        """
        variation = super(ProductOptionGroupsViewMixin, self).get_variation()
        variation.update({ 'option_groups': {} })
        product = self.get_object()
        for option_group in product.options_groups.all():
            key = 'add_item_option_group_%s' % option_group.id
            if self.request.POST.has_key(key):
                key = int(self.request.POST[key])
                value = option_group.__dict__
                del value['_state']
                value['option'] = Option.objects.get(pk=key).__dict__
                del value['option']['_state']
                variation['option_groups'][option_group.id] = value
        return variation

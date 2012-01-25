# -*- coding: utf-8 -*-


class ProductTextOptionsViewMixin(object):
    """
    DetailView Mixin class when using ProductTextOptionsMixin
    """

    def get_variation(self, product):
        """
        The post request contains information about the chosen variation.
        Recombine this with the information extracted from the OptionGroup
        for the given product
        """
        variation = { 'text_options': {} }
        basevar = super(ProductTextOptionsViewMixin, self).get_variation(product)
        if basevar is not None:
            variation.update(basevar)
        for text_option in product.text_options.all():
            key = 'add_item_text_option_%s' % text_option.id
            if self.request.POST.has_key(key):
                value = text_option.__dict__
                del value['_state']
                value['text'] = self.request.POST[key]
                variation['text_options'][text_option.id] = value
        return variation

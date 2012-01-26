===============================
django SHOP - Variable Products
===============================

This app's purpose is to provide two product mixin classes together with two 
corresponding view mixin classes. They offers two simple product variations
variants. They can be used as a stand-alone app or as a starting point how
to add a self contained variation to a product.

Currently two variation variants are implemented

Option groups
=============
One or more groups of options may be assigned to a product. Such a group can be
something like color, wrapping paper, etc. Each of these groups can have two or
more options, say for group color: red, pink, yellow, magenta.

The shop owner may specify for each product, which option groups shall belong to
it. To each option, an additional price can be added. 

While filling the shopping cart, the customer then may chose one of these
options using a select box.

Text options
============
One or more text options may be assigned to a product. Such an option can be
something such as an individual engraving or a congratulation message. An
additional price may be added per character.

While filling the shopping cart, the customer then may add an individual text
message to the product he intends to buy.


Installation
------------
This requires a patched version of django SHOP (https://github.com/jrief/django-shop/tree/variations)
which offers a simpler interface to products variations.

* Add `shop_product_optiongroups` and/or to `shop_product_textoptions` your
  INSTALLED_APPS of your settings.py.
* Add `shop_product_optiongroups.cart_modifier.OptionGroupsCartModifier`
  and/or `shop_product_textoptions.cart_modifier.TextOptionsOptionsCartModifier`
  to your SHOP_CART_MODIFIERS of your settings.py.

Usage
-----

Run schemamigration for `shop_product_optiongroups` and `shop_product_textoptions`
and migrate those schemas.

Change your code
================

Add to your product model one or both of these mixin classes::

   from shop.models.productmodel import Product
   from shop_product_optiongroups.models import ProductOptionGroupsMixin
   from shop_product_textoptions.models import ProductTextOptionsMixin
   
   class MyProduct(Product, ProductOptionGroupsMixin, ProductTextOptionsMixin):
       ...


Add to your product's detail view one or both of these mixin classes::

   from shop.views.product import ProductDetailView
   from shop_product_optiongroups.views import ProductOptionGroupsViewMixin
   from shop_product_textoptions.views import ProductTextOptionsViewMixin
   
   class MyProductDetailView(ProductOptionGroupsViewMixin, \
      ProductTextOptionsViewMixin, ProductDetailView):


Override django-shop's `product_detail.html` template and add selection elements
so that your users can select these variations. Use the prepared template tags
for this purpose::

   {% load product_optiongroups product_textoptions %}
   ...
   {% with option_groups=object|get_option_groups %}
   {% if option_groups %}
   <div>
     <h2>Variations:</h2>
     {% for option_group in option_groups %}
     <label for="add_item_option_group_{{ option_group.id }}">{{ option_group.name }}:</label>
     {% with option_group|get_options as options %}
     <select name="add_item_option_group_{{ option_group.id }}">
       {% for option in options %}
       <option value="{{ option.id }}">{{ option.name }}</option>
       {% endfor %}
     </select>
     {% endwith %}
     {% endfor %}
   </div>
   {% endif %}
   {% endwith %}
   ...
   {% with text_options=object.text_options.all %}
   {% if text_options %}
   <div>
     <h2>Text options:</h2>
     {% for text_option in text_options %}
     <label for="add_item_text_option_{{ text_option.id }}">{{ text_option.name }}:</label>
     <input type="text" name="add_item_text_option_{{ text_option.id }}" value="" />
     {% endfor %}
   </div>
   {% endif %}
   {% endwith %}


Fill your database
==================

* Log into the admin interface.
* Go to Shop_Product_Optiongroups.
* Add an Option Group and add Options to this group.
* Go to Shop_Product_Textoptions.
* Add a Text Option.


Contributing
============

Feel free to fork this project on github, send pull requests...
development discussion happends on the django SHOP mailing list
https://groups.google.com/forum/#!forum/django-shop

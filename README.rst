===============================
django SHOP - Variable Products
===============================

This app's purpose is to provide a products base class which offers two simple
product variations variants. It can be used as a stand-alone app or as an 
example how to add any complex variaion to a product.

It considers variations as a {label: value} entry in the products detail view,
so it is perfect for things like differently priced colors, or customized
text on the product itself.


Installation
============

This requires a patched version of django SHOP (https://github.com/jrief/django-shop/tree/variations)
which offers a simpler interface to products variations.

* Add the app to your INSTALLED_APPS in your settings.py
* Add `shop_productvariations.cart_modifier.ProductOptionsModifier` to your
  `SHOP_CART_MODIFIERS` setting.


Usage
=====

Change your code
* derive your product's model definition from
 `shop_productvariations.models.VariableProduct`.
* run `manage.py schemamigration` for your app and shop_productvariations and 
  migrate those schemas.
* Override django-shop's `product_detail.html` template and add selection
  elements so that your users can select variations.

In the admin view
* create an Option group.
* add options and the corresponding price to the group.
* add a Text option.
* choose which Text options and/or which Option groups shall be available for
  each specific products kind.


The product_detail.html template
================================
The simple `product_detail.html` that ships with the shop doesn't take
variations into consideration.

Therefore you need to override the template. django-shop-productvariations
ships with two templatetags that help creating drop down lists so that a
customer can actually chose variation.

First make sure to load the simplevariation templatetags:

::

  {% load simplevariation_tags %}
  <h1>Product detail:</h1>
  ...

Next create the drop down lists of OptionsGroups and Options:

::

   <form method="post" action="{% url your_product_detail object.slug %}">{% csrf_token %}
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
     <p>
       <input type="hidden" name="add_item_id" value="{{object.id}}">
       <input type="hidden" name="add_item_quantity" value="1">
       <button type="submit" name="add_to" value="cart">Add to cart</button>
       <button type="submit" name="add_to" value="wishlist">Add to wishlist</button>  
     </p>
   </form>

Contributing
============

Feel free to fork this project on github, send pull requests...
development discussion happends on the django SHOP mailing list
(django-shop@googlegroups.com)

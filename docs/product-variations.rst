How to add variations to a product
==================================

From django-shop-simplevariations to django-shop-productvariations
------------------------------------------------------------------
django-shop ships with an additional module (django-shop-simplevariations) to
add two kind of variations: ``Option group`` and ``Text option``. This module can
be used as an add on for any kind of product. The problem however is, that all
variations are stored in relational models, making it difficult to move a
product item from the cart to the order or vice versa. When implementing
functionality for, say a wishlist or a comparison cart, additional tables would
have to be added, in order to keep track of the kind of desired variation.

When adding two or more products to the cart, it is quite difficult to determine
if a desired product is equal, or a variation of an existing product, and thus
shall be represented as identical or different items on the cart.

By using the built-in variations, the product model itself, may specify any kind
of thinkable variations. This variation model transparently integrates into the
checkout process of the shop.

The benefits for built-in variations:

* The variation definition is part of the product model.
* Any kind of information can be stored together with the product.
* Identical variations are always serialized to the same string, so identical
  product variations will sum up in CartItem, whereas different variations of 
  the same product create individual CartItem entries.
* A customer may re-add an already shipped item from the list of orders to the 
  cart.
* The product model must not deal with problems, such as adding variation
  details to the CartItem, OrderItem or an external WishItem.

When using the django-shop-wishlists, built-in variations are a required 
feature.

django-shop-productvariations is a reimplementation of django-shop-simplevariations,
which makes usage of that additional field.

# -*- coding: utf-8 -*-
from decimal import Decimal
from jsonfield.fields import JSONField
from django.test import TestCase
from django.contrib.auth.models import User
from django.core.serializers.json import DjangoJSONEncoder
from django.http import HttpResponseRedirect
from django.utils import simplejson as json
from shop.models import Cart, CartItem
from shop_productvariations.models import Option, OptionGroup, TextOption
from shop.views.cart import CartDetails
from shop.tests.util import Mock
from project.models import DiaryProduct
from project.views import DiaryDetailView


class ProductVariationsTest(TestCase):    
    def setUp(self):
        """Sets up the TestModel."""
        self._create_options()
        self.product = DiaryProduct(isbn='1234567890', number_of_pages=100)
        self.product.name = 'test'
        self.product.slug = 'test'
        self.product.short_description = 'test'
        self.product.long_description = 'test'
        self.product.unit_price = Decimal('1.0')
        self.product.save()
        options_group = OptionGroup.objects.all()[0]
        self.product.options_groups.add(options_group)
        text_options = TextOption.objects.all()[0]
        self.product.text_options.add(text_options)
        self.user = User.objects.create(username="test",
                                        email="test@example.com",
                                        first_name="Test",
                                        last_name="Tester")

    def test_get_product_returns_correctly(self):
        request = Mock()
        view = DiaryDetailView(request=request, kwargs={'pk': self.product.id})
        setattr(view, 'object', None)
        obj = view.get_object()
        self.assertTrue(isinstance(obj, DiaryProduct))

    def test_get_templates_return_expected_values(self):
        view = DiaryDetailView()
        setattr(view, 'object', None)
        tmp = view.get_template_names()
        self.assertEqual(len(tmp), 1)

    def test_add_to_cart(self):
        request = Mock()
        setattr(request, 'is_ajax', lambda: False)
        setattr(request, 'user', self.user)
        
        # first, add the product together with its variations
        post = {
            'add_item_id': self.product.id,
            'add_item_quantity': 1,
            'add_item_option_group_1': 2, # Color: green
            'add_item_text_option_1': 'Doctor Diary', # Engraving
        }
        setattr(request, 'POST', post)
        diary_view = DiaryDetailView(request=request, kwargs={'pk': self.product.id})
        setattr(diary_view, 'object', None)
        ret = diary_view.post()
        self.assertTrue(isinstance(ret, HttpResponseRedirect))

        # then check if the product is in the cart
        request = Mock()
        setattr(request, 'user', self.user)
        cart_view = CartDetails(request=request)
        ret = cart_view.get_context_data()
        self.assertNotEqual(ret, None)
        self.assertEqual(len(ret['cart_items']), 1)
        values = ret['cart_items'].values()[0]
        self.assertEqual(values['product_id'], self.product.id)
        self.assertEqual(values['quantity'], 1)
        variation = json.loads(values['variation'])
        self.assertEqual(variation['option_groups']['1']['name'], 'Color')
        self.assertEqual(variation['option_groups']['1']['option']['name'], 'green')
        self.assertEqual(variation['text_options']['1']['text'], 'Doctor Diary')

        # add the same item again
        diary_view.post()
        ret = cart_view.get_context_data()
        self.assertNotEqual(ret, None)
        self.assertEqual(len(ret['cart_items']), 1)
        values = ret['cart_items'].values()[0]
        self.assertEqual(values['quantity'], 2)

    def _create_options(self):
        option_group = OptionGroup(name='Color', slug='color')
        option_group.save()
        price = Decimal('1.25')
        Option(name='red', price=price, group=option_group).save()
        Option(name='green', price=price, group=option_group).save()
        Option(name='blue', price=price, group=option_group).save()
        TextOption(name='Engraving', price=price, max_length=12).save()

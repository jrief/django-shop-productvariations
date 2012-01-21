# -*- coding: utf-8 -*-
from decimal import Decimal
from django.test import TestCase
from django.contrib.auth.models import User
from django.utils import simplejson as json
from shop_productvariations.models import Option, OptionGroup, TextOption
from shop.views.cart import CartDetails
from shop.tests.util import Mock
from models import DiaryProduct
from views import DiaryDetailView


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
        self.assertGreaterEqual(len(tmp), 1)

    def test_add_to_cart_using_post(self):
        # create form data with a product containing variations and simulate POST
        post = {
            'product_action': 'add_to_cart',
            'add_item_id': self.product.id,
            'add_item_quantity': 1,
            'add_item_option_group_1': 2, # Color: green
            'add_item_text_option_1': 'Doctor Diary', # Engraving
        }
        self._add_to_cart(post)
        ret = self._get_from_cart()

        # check if the product is in the cart
        self.assertEqual(len(ret['cart_items']), 1)
        values = ret['cart_items'].values()[0]
        self.assertEqual(values['product_id'], self.product.id)
        self.assertEqual(values['quantity'], 1)
        variation = json.loads(values['variation'])
        self.assertEqual(variation['option_groups']['1']['name'], 'Color')
        self.assertEqual(variation['option_groups']['1']['option']['name'], 'green')
        self.assertEqual(variation['text_options']['1']['text'], 'Doctor Diary')

        # add the same product with missing quantity field
        del post['add_item_quantity']
        self._add_to_cart(post)
        ret = self._get_from_cart()
        values = ret['cart_items'].values()[0]
        self.assertEqual(values['quantity'], 2)        

    def _add_to_cart(self, post):
        request = Mock()
        setattr(request, 'is_ajax', lambda: False)
        setattr(request, 'user', self.user)
        setattr(request, 'POST', post)
        view = DiaryDetailView(request=request, kwargs={'pk': self.product.id})
        setattr(view, 'object', None)
        view.post()
        
    def _get_from_cart(self):
        request = Mock()
        setattr(request, 'user', self.user)
        view = CartDetails(request=request)
        ret = view.get_context_data()
        self.assertNotEqual(ret, None)
        return ret

    def _create_options(self):
        option_group = OptionGroup(name='Color', slug='color')
        option_group.save()
        price = Decimal('1.25')
        Option(name='red', price=price, group=option_group).save()
        Option(name='green', price=price, group=option_group).save()
        Option(name='blue', price=price, group=option_group).save()
        TextOption(name='Engraving', price=price, max_length=12).save()

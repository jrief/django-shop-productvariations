# -*- coding: utf-8 -*-
from decimal import Decimal
from django.test import TestCase
from django.contrib.auth.models import User
from django.utils import simplejson as json
from shop_product_optiongroups.models import Option, OptionGroup
from shop_product_textoptions.models import TextOption
from shop.views.cart import CartDetails
from shop.tests.util import Mock
from models import DiaryProduct, CalendarProduct
from views import DiaryDetailView, CalendarDetailView


class ProductVariationsTest(TestCase):    
    def setUp(self):
        """Sets up the TestModel."""
        self._create_options()
        self._create_mock_diary()
        self._create_mock_calendar()
        self.user = User.objects.create(username="test",
                                        email="test@example.com",
                                        first_name="Test",
                                        last_name="Tester")

    def test_get_product_returns_correctly(self):
        request = Mock()
        view = DiaryDetailView(request=request, kwargs={'pk': self.diary.id})
        setattr(view, 'object', None)
        obj = view.get_object()
        self.assertTrue(isinstance(obj, DiaryProduct))

    def test_get_templates_return_expected_values(self):
        view = DiaryDetailView()
        setattr(view, 'object', None)
        tmp = view.get_template_names()
        self.assertGreaterEqual(len(tmp), 1)

    def test_add_diary_to_cart_using_post(self):
        # create form data with a product containing variations and simulate POST
        post = {
            'product_action': 'add_to_cart',
            'add_item_id': self.diary.id,
            'add_item_quantity': 1,
            'add_item_option_group_1': 2, # Color: green
            'add_item_text_option_1': 'Doctor Diary', # Engraving
        }
        request = self._get_post_request(post)
        view = DiaryDetailView(request=request, kwargs={'pk': self.diary.id})
        view.post()
        ret = self._get_from_cart()

        # check if the product is in the cart
        self.assertEqual(len(ret['cart_items']), 1)
        values = ret['cart_items'].values()[0]
        self.assertEqual(values['product_id'], self.diary.id)
        self.assertEqual(values['quantity'], 1)
        variation = json.loads(values['variation'])
        self.assertEqual(variation['option_groups']['1']['name'], 'Color')
        self.assertEqual(variation['option_groups']['1']['option']['name'], 'green')
        self.assertEqual(variation['text_options']['1']['text'], 'Doctor Diary')

        # add the same product with missing quantity field
        del post['add_item_quantity']
        request = self._get_post_request(post)
        view = DiaryDetailView(request=request, kwargs={'pk': self.diary.id})
        view.post()
        ret = self._get_from_cart()
        values = ret['cart_items'].values()[0]
        self.assertEqual(values['quantity'], 2)        

    def test_add_calendar_to_cart_using_post(self):
        # create form data with a product containing variations and simulate POST
        post = {
            'product_action': 'add_to_cart',
            'add_item_id': self.calendar.id,
            'add_item_quantity': 1,
            'add_item_option_group_1': 1, # Color: red
        }
        request = self._get_post_request(post)
        view = CalendarDetailView(request=request, kwargs={'pk': self.calendar.id})
        setattr(view, 'object', None)
        view.post()
        ret = self._get_from_cart()

        # check if the product is in the cart
        self.assertEqual(len(ret['cart_items']), 1)
        values = ret['cart_items'].values()[0]
        self.assertEqual(values['product_id'], self.calendar.id)
        self.assertEqual(values['quantity'], 1)
        variation = json.loads(values['variation'])
        self.assertEqual(variation['option_groups']['1']['name'], 'Color')
        self.assertEqual(variation['option_groups']['1']['option']['name'], 'red')
        self.assertFalse('text_options' in variation)

    def _get_post_request(self, post):
        request = Mock()
        setattr(request, 'is_ajax', lambda: False)
        setattr(request, 'user', self.user)
        setattr(request, 'POST', post)
        return request
        
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

    def _create_mock_diary(self):
        self.diary = DiaryProduct(isbn='1234567890', number_of_pages=100)
        self.diary.name = 'Diary'
        self.diary.slug = 'mock-diary'
        self.diary.short_description = 'test'
        self.diary.long_description = 'test'
        self.diary.unit_price = Decimal('1.0')
        self.diary.save()
        options_group = OptionGroup.objects.all()[0]
        self.diary.options_groups.add(options_group)
        text_options = TextOption.objects.all()[0]
        self.diary.text_options.add(text_options)

    def _create_mock_calendar(self):
        self.calendar = CalendarProduct(isbn='1234567890', number_of_pages=100)
        self.calendar.name = 'Calendar'
        self.calendar.slug = 'mock-calendar'
        self.calendar.short_description = 'test'
        self.calendar.long_description = 'test'
        self.calendar.unit_price = Decimal('1.0')
        self.calendar.save()
        options_group = OptionGroup.objects.all()[0]
        self.calendar.options_groups.add(options_group)

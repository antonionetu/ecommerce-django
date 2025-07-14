import json
from unittest.mock import patch

from django.test import TestCase
from django.urls import reverse

from .. import utils


class ProductsViewTestCase(TestCase):
    def setUp(self):
        utils.create_products()
        self.response = self.client.get(
            reverse('products')
        )

    def test_render_page(self):
        self.assertEqual(self.response.status_code, 200)
        self.assertEqual(len(self.response.context['products']), 8)
        
    def test_strategy(self):
        self.response = self.client.get(
            reverse('products') + "?p=2"
        )
        json_response = json.loads(self.response._container[0].decode('utf-8'))

        self.assertEqual(self.response.status_code, 200)
        self.assertIsNone(self.response.context)
        self.assertIsNotNone(self.response.json)
        self.assertEqual(len(json_response), 8)

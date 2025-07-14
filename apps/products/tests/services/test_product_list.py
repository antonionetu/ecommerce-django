import json
from unittest.mock import patch

from django.test import TestCase
from django.urls import reverse

from ... import services

from .. import utils


class ProductListServiceTestCase(TestCase):
    def setUp(self):
        self.products = utils.create_products()

    def test_service(self):
        response = services.product_list.service('req')
        self.assertEqual(len(response), 8)

    def test_service_limit_quantity(self):
        response = services.product_list.service('req', quantity=4)
        self.assertEqual(len(response), 4)

    def test_service_change_page(self):
        response_page_1 = services.product_list.service('req')
        response_page_2 = services.product_list.service('req', page=2)
        self.assertEqual(len(response_page_1), 8)
        self.assertEqual(len(response_page_1), len(response_page_2))
        self.assertNotEqual(response_page_1, response_page_2)

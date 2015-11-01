from unittest import TestCase
from mock import patch, call

# This module is imported in the test but has nothing to do with the product
import os
import product

class ProductTest(TestCase):
    def setUp(self):
        self.instance = product.MainClass()

    def test_one(self):
        tester = product.Delegate()
        self.assertEquals(True, tester.business_logic(42))
        self.assertEquals('False', tester.business_logic(41))

    @patch('product.print')
    def test_two(self, mock_print):
        self.instance.dispatcher(42)
        self.assertEquals([call(34)], mock_print.mock_calls)

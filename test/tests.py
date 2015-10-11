from unittest import TestCase
from mock import patch, call

# This module is imported in the test but has nothing to do with the product
import os
import product

class ProductTest(TestCase):
    def setUp(self):
        self.instance = product.MainClass()

    def test_one(self):
        tester = product.Tester()
        self.assertEquals(True, tester.test(42))
        self.assertEquals('False', tester.test(41))
        #self.fail()

    @patch('product.print')
    def test_two(self, mock_print):
        self.instance.dispatcher(42)
        self.assertEquals([call(34)], mock_print.mock_calls)

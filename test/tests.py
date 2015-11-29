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

    def test_two(self):
        self.assertEquals(
            34,
            self.instance.dispatcher(42)
        )

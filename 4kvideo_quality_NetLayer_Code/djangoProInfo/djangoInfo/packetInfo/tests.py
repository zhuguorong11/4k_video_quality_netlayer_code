# from django.test import TestCase
import unittest
# Create your tests here.
class SimpleTest(unittest.TestCase):
    def test_basic_addition(self):
        self.assertEqual(1 + 11,12)
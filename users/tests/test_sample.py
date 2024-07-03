from django.test import TestCase

class SimpleTestCase(TestCase):
    def test_addition(self):
        self.assertFalse(2 + 3 == 10)
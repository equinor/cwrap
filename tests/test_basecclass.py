import unittest

from cwrap import BaseCClass


class BaseCClassTest(unittest.TestCase):
    def test_creation(self):
        with self.assertRaises(ValueError):
            obj = BaseCClass(0)

        obj = BaseCClass(10)
        self.assertTrue(obj)

        obj._invalidateCPointer()
        self.assertFalse(obj)

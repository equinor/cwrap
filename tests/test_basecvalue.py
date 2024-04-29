import os
import unittest
from ctypes import c_double, c_ubyte

from cwrap import BaseCValue, Prototype, load


class ForTestPrototype(Prototype):
    lib = load("msvcrt" if os.name == "nt" else None)

    def __init__(self, prototype):
        super().__init__(self.lib, prototype)


class UnsignedByteValue(BaseCValue):
    DATA_TYPE = c_ubyte


class SqrtDouble(BaseCValue):
    TYPE_NAME = "sqrt_double"
    DATA_TYPE = c_double


class BaseCValueTest(unittest.TestCase):
    def setUp(self):
        self.sqrt_double = ForTestPrototype("sqrt_double sqrt(double)")

    def test_illegal_type(self):
        class ExceptionValueTest(BaseCValue):
            DATA_TYPE = str

            def __init__(self, value):
                super().__init__(value)

        with self.assertRaises(ValueError):
            ExceptionValueTest("Failure")

        class NoDataTypeTest(BaseCValue):
            def __init__(self, value):
                super().__init__(value)

        with self.assertRaises(ValueError):
            ExceptionValueTest(0)

    def test_creation(self):
        test_value = UnsignedByteValue(255)

        self.assertEqual(test_value.value(), 255)

        test_value.setValue(256)
        self.assertEqual(test_value.value(), 0)

        self.assertEqual(test_value.type(), c_ubyte)

    def test_from_param(self):
        test_value = UnsignedByteValue(127)

        self.assertEqual(UnsignedByteValue.from_param(test_value).value, 127)

        with self.assertRaises(AttributeError):
            UnsignedByteValue.from_param(None)

        with self.assertRaises(ValueError):
            UnsignedByteValue.from_param("exception")

    def test_double_sqrt(self):
        sqrt_value = self.sqrt_double(100)

        self.assertIsInstance(sqrt_value, SqrtDouble)
        self.assertEqual(sqrt_value.value(), 10)

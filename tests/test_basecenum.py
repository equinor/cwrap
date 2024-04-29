import ctypes
import os
import unittest

from cwrap import BaseCEnum, Prototype, load


class BaseCEnumTest(unittest.TestCase):
    def test_base_c_enum(self):
        class enum(BaseCEnum):
            pass

        enum.addEnum("ONE", 1)
        enum.addEnum("TWO", 2)
        enum.addEnum("THREE", 3)
        enum.addEnum("FOUR", 4)

        class enum2(BaseCEnum):
            pass

        enum2.addEnum("ONE", 1)
        enum2.addEnum("TWO", 4)

        self.assertEqual(enum.ONE, 1)
        self.assertEqual(enum.TWO, 2)
        self.assertEqual(enum.FOUR, 4)

        self.assertListEqual(enum.enums(), [enum.ONE, enum.TWO, enum.THREE, enum.FOUR])

        self.assertEqual(enum(4), enum.FOUR)

        self.assertNotEqual(enum2(4), enum.FOUR)
        self.assertEqual(enum2(4), enum2.TWO)

        self.assertEqual(str(enum.ONE), "ONE")

        self.assertEqual(enum.ONE + enum.TWO, enum.THREE)
        self.assertEqual(enum.ONE + enum.FOUR, 5)

        with self.assertRaises(ValueError):
            e = enum(5)

        self.assertEqual(enum.THREE & enum.ONE, enum.ONE)
        self.assertEqual(enum.ONE | enum.TWO, enum.THREE)
        self.assertEqual(enum.THREE ^ enum.TWO, enum.ONE)

        with self.assertRaises(AssertionError):
            e = enum.ONE + enum2.ONE

        with self.assertRaises(AssertionError):
            e = enum.ONE & enum2.ONE

        with self.assertRaises(AssertionError):
            e = enum.ONE | enum2.ONE

        with self.assertRaises(AssertionError):
            e = enum.ONE ^ enum2.ONE  # noqa F841

    def test_in_operator(self):
        class PowerOf2(BaseCEnum):
            pass

        PowerOf2.addEnum("ONE", 1)
        PowerOf2.addEnum("TWO", 2)
        PowerOf2.addEnum("FOUR", 4)

        three = PowerOf2.ONE | PowerOf2.TWO

        self.assertEqual(int(three), 3)

        self.assertIn(PowerOf2.TWO, three)
        self.assertIn(PowerOf2.ONE, three)
        self.assertNotIn(PowerOf2.FOUR, three)

    def test_repr_and_str(self):
        class MyLonelyEnum(BaseCEnum):
            pass

        MyLonelyEnum.addEnum("ONE", 1)
        MyLonelyEnum.addEnum("TWO", 2)
        MyLonelyEnum.addEnum("THREE", 3)
        MyLonelyEnum.addEnum("FOUR", 4)

        tri = MyLonelyEnum.THREE

        self.assertEqual(repr(tri), 'MyLonelyEnum(name = "THREE", value = 3)')
        self.assertEqual(str(tri), "THREE")
        self.assertEqual(tri.name, "THREE")
        self.assertEqual(tri.value, 3)

    def test_from_name(self):
        class EnumName(BaseCEnum):
            pass

        EnumName.addEnum("ONE", 1)
        EnumName.addEnum("TWO", 2)

        with self.assertRaises(ValueError):
            EnumName.from_string("No-not-this")

        one = EnumName.from_string("ONE")
        self.assertEqual(one, EnumName.ONE)


def test_that_enum_can_be_bind_methods():
    class LibCPrototype(Prototype):
        lib = load("msvcrt" if os.name == "nt" else None)

        def __init__(self, prototype, bind=False, allow_attribute_error=False):
            super().__init__(
                LibCPrototype.lib,
                prototype,
                bind=bind,
                allow_attribute_error=allow_attribute_error,
            )

    class Endumb(BaseCEnum):
        TYPE_NAME = "endumb"
        SOME_VALUE = None
        SOME_OTHER_VALUE = None
        abs = LibCPrototype("int abs(endumb)", bind=True)

    Endumb.addEnum("SOME_VALUE", -1)
    assert Endumb.SOME_VALUE.abs() == 1


def test_base_c_enum_to_c_int():
    class NumberEnum(BaseCEnum):
        pass

    NumberEnum.addEnum("ONE", 1)

    c_int_value = ctypes.c_int(NumberEnum.ONE)
    assert c_int_value.value == NumberEnum.ONE

from unittest import TestCase

from cwrap import BaseCEnum


class Enum(BaseCEnum):
    ONE = 1
    TWO = 2
    FOUR = 4
    THREE = 3


class AnotherEnum(BaseCEnum):
    ONE = 1
    TWO = 4


class BaseCEnumTest(TestCase):
    def test_base_c_enum(self):
        self.assertIsInstance(Enum.ONE, Enum)
        self.assertIsInstance(AnotherEnum.ONE, AnotherEnum)

        self.assertEqual(Enum.ONE, 1)
        self.assertEqual(Enum.TWO, 2)
        self.assertEqual(Enum.FOUR, 4)

        self.assertListEqual(Enum.enums(), [Enum.ONE, Enum.TWO, Enum.THREE, Enum.FOUR])

        self.assertEqual(Enum(4), Enum.FOUR)

        self.assertNotEqual(AnotherEnum(4), Enum.FOUR)
        self.assertEqual(AnotherEnum(4), AnotherEnum.TWO)

        self.assertEqual(str(Enum.ONE), "ONE")

        self.assertEqual(Enum.ONE + Enum.TWO, Enum.THREE)
        self.assertEqual(Enum.ONE + Enum.FOUR, 5)

        with self.assertRaises(ValueError):
            e = Enum(5)

        self.assertEqual(Enum.THREE & Enum.ONE, Enum.ONE)
        self.assertEqual(Enum.ONE | Enum.TWO, Enum.THREE)
        self.assertEqual(Enum.THREE ^ Enum.TWO, Enum.ONE)

        with self.assertRaises(AssertionError):
            e = Enum.ONE + AnotherEnum.ONE

        with self.assertRaises(AssertionError):
            e = Enum.ONE & AnotherEnum.ONE

        with self.assertRaises(AssertionError):
            e = Enum.ONE | AnotherEnum.ONE

        with self.assertRaises(AssertionError):
            e = Enum.ONE ^ AnotherEnum.ONE


    def test_in_operator(self):
        class PowerOf2(BaseCEnum):
            ONE = 1
            TWO = 2
            FOUR = 4

        three = PowerOf2.ONE | PowerOf2.TWO

        self.assertEqual(int(three), 3)

        self.assertIn(PowerOf2.TWO, three)
        self.assertIn(PowerOf2.ONE, three)
        self.assertNotIn(PowerOf2.FOUR, three)

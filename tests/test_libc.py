import os
import unittest

from cwrap import BaseCClass, Prototype, load


class LibCPrototype(Prototype):
    lib = load("msvcrt" if os.name == "nt" else None)

    def __init__(self, prototype, bind=False, allow_attribute_error=False):
        super().__init__(
            LibCPrototype.lib,
            prototype,
            bind=bind,
            allow_attribute_error=allow_attribute_error,
        )


class LibC(BaseCClass):
    TYPE_NAME = "void_libc_none"
    _malloc = LibCPrototype("void* malloc(void*)")
    _abs = LibCPrototype("int   abs(int)")
    _atoi = LibCPrototype("int   atoi(char*)")
    _strchr = LibCPrototype("char* strchr(char*, int)")
    _free = LibCPrototype("void  free(void*)")
    _missing_function = LibCPrototype(
        "void  missing_function(int*)", allow_attribute_error=True
    )

    def __init__(self):
        c_ptr = 1  # c_ptr = self._malloc(4)
        super().__init__(c_ptr)

    def abs(self, x):
        return self._abs(x)

    def atoi(self, s):
        return self._atoi(s)

    def strchr(self, s, t):
        return self._strchr(s, t)

    def free(self):
        pass  # self._free(self.__c_pointer)


class LibCTest(unittest.TestCase):
    def test_libc(self):
        lib = LibC()
        self.assertEqual(lib.abs(-3), 3)
        self.assertEqual(lib.abs(0), 0)
        self.assertEqual(lib.abs(42), 42)
        self.assertEqual(lib.atoi("12"), 12)
        self.assertEqual(lib.atoi("-100"), -100)
        self.assertEqual(lib.strchr("a,b", ord(",")), ",b")
        self.assertEqual(lib.strchr("a,b", ord("x")), None)

        with self.assertRaises(NotImplementedError):
            lib._missing_function(100)

        with self.assertRaises(TypeError):
            self.assertEqual(lib.abs("SPAM"), 3)

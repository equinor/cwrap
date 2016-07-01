import ctypes
from cwrap import BaseCClass, Prototype
from cwrap.clib import lib_name


class LibCPrototype(Prototype):
    _LIB_NAME = "libc"

    lib_file = lib_name( _LIB_NAME )
    if not lib_file:
        raise ImportError("Cannot find library " + _LIB_NAME )
    lib = ctypes.CDLL( lib_file , ctypes.RTLD_GLOBAL )

    def __init__(self , prototype , bind = True):
        super(LibCPrototype , self).__init__( LibCPrototype.lib , prototype , bind = bind)


class LibC(BaseCClass):
    """

    """
    TYPE_NAME = "libc"

    _malloc  = LibCPrototype("void* malloc(void*)", bind=False)
    _abs    = LibCPrototype("int   abs(int)", bind=False)
    _atoi   = LibCPrototype("int   atoi(char*)", bind=False)
    _free   = LibCPrototype("void  free(void*)", bind=False)

    def __init__(self):
        c_ptr = 1#c_ptr = self._malloc(4)
        super(LibC, self).__init__(c_ptr)

    def abs(self, x):
        return self._abs(x)

    def atoi(self, s):
        return self._atoi(s)

    def free(self):
        pass#self._free(self.__c_pointer)

lib = LibC()
assert lib.abs(-3) == 3
assert lib.abs(0) == 0
assert lib.abs(42) == 42
assert lib.atoi("12") == 12
assert lib.atoi("-100") == -100
print "yes, |-18| =", lib.abs(-18)

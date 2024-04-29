import ctypes
from cwrap import BaseCClass, Prototype
from cwrap.clib import lib_name


class ExMapPrototype(Prototype):
    _LIB_NAME = "ex_map"

    lib_file = lib_name(_LIB_NAME)
    if not lib_file:
        raise ImportError("Cannot find library " + _LIB_NAME)
    lib = ctypes.CDLL(lib_file, ctypes.RTLD_GLOBAL)

    def __init__(self, prototype, bind=True):
        super(ExMapPrototype, self).__init__(ExMapPrototype.lib, prototype, bind=bind)


class ExMap(BaseCClass):
    """
    Super thin wrapper around a std::map<char*, int>.
    """

    TYPE_NAME = "ex_map"

    _alloc = ExMapPrototype("void* ex_map_alloc()", bind=False)
    _free = ExMapPrototype("void  ex_map_free(ex_map)")
    _size = ExMapPrototype("int   ex_map_size(ex_map)")
    _insert = ExMapPrototype("void  ex_map_insert(ex_map, char*, int)")
    _find = ExMapPrototype("int   ex_map_find(ex_map, char*)")
    _count = ExMapPrototype("int   ex_map_count(ex_map, char*)")
    _at = ExMapPrototype("char* ex_map_get_key_at(ex_map, int)")

    def __init__(self):
        c_ptr = self._alloc()
        super(ExMap, self).__init__(c_ptr)

    def keys(self):
        return [self._at(i) for i in range(len(self))]

    def __len__(self):
        return self._size()

    def __setitem__(self, key, val):
        self._insert(key, val)

    def __contains__(self, key):
        return self._count(key) > 0

    def __getitem__(self, key):
        if key in self:
            return self._find(key)
        else:
            raise KeyError("Key %s not found in map" % key)

    def __str__(self):
        ks = self.keys()
        kv = ["'%s': %s" % (k, self[k]) for k in ks]
        return "{%s}" % (", ".join(kv))

    def free(self):
        self._free()


em = ExMap()
em["Abc"] = 42
em["Jean-Paul"] = 3
em["cwrap"] = 2
em["jokva"] = 17

if em["Abc"] != 42:
    print("Test failure.")

if len(em) != 4:
    print("Test fail")

print(em)

import ctypes


class ExMap:
    lib = ctypes.CDLL("ex_map.dylib")

    lib.ex_map_alloc.restype = ctypes.c_void_p
    lib.ex_map_alloc.argtypes = []

    lib.ex_map_free.restype = None
    lib.ex_map_free.argtypes = [ctypes.c_void_p]

    lib.ex_map_size.restype = ctypes.c_int
    lib.ex_map_size.argtypes = [ctypes.c_void_p]

    lib.ex_map_insert.restype = None
    lib.ex_map_insert.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_int]

    lib.ex_map_find.restype = ctypes.c_int
    lib.ex_map_find.argtypes = [ctypes.c_void_p, ctypes.c_char_p]

    lib.ex_map_count.restype = ctypes.c_int
    lib.ex_map_count.argtypes = [ctypes.c_void_p, ctypes.c_char_p]

    lib.ex_map_get_key_at.restype = ctypes.c_char_p
    lib.ex_map_get_key_at.argtypes = [ctypes.c_void_p, ctypes.c_int]

    def __init__(self):
        self.map_ptr = ExMap.lib.ex_map_alloc()

    def keys(self):
        return [self._at(i) for i in range(len(self))]

    def free(self):
        ExMap.lib.ex_map_free(self.map_ptr)

    def _size(self):
        return ExMap.lib.ex_map_size(self.map_ptr)

    def _insert(self, key, value):
        ExMap.lib.ex_map_insert(self.map_ptr, key.encode("utf-8"), value)

    def _find(self, key):
        return ExMap.lib.ex_map_find(self.map_ptr, key.encode("utf-8"))

    def _count(self, key):
        return ExMap.lib.ex_map_count(self.map_ptr, key.encode("utf-8"))

    def _at(self, idx):
        return ExMap.lib.ex_map_get_key_at(self.map_ptr, ctypes.c_int(idx)).decode(
            "utf-8"
        )

    def __len__(self):
        return self._size()

    def __setitem__(self, key, val):
        self._insert(key, val)

    def __getitem__(self, key):
        if key in self:
            return self._find(key)
        else:
            raise KeyError("Key %s not found in map" % key)

    def __contains__(self, key):
        return self._count(key) > 0

    def __str__(self):
        ks = self.keys()
        kv = ["'%s': %s" % (k, self[k]) for k in ks]
        return "{%s}" % (", ".join(kv))


em = ExMap()

em["Abc"] = 42
em["Jean-Paul"] = 3
em["cwrap"] = 2
em["jokva"] = 17

assert em._at(0) == "Abc", "Test failure..."
assert "Abc" in em, "Test failure..."
assert em["Abc"] == 42, "Test failure..."

assert ["Abc", "Jean-Paul", "cwrap", "jokva"] == [key for key in em.keys()]

em.free()

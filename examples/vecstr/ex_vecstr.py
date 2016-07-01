import ctypes
from cwrap import BaseCClass, Prototype
from cwrap.clib import lib_name


class ExVecstrPrototype(Prototype):
    _LIB_NAME = "ex_vecstr"

    lib_file = lib_name( _LIB_NAME )
    if not lib_file:
        raise ImportError("Cannot find library " + _LIB_NAME )
    lib = ctypes.CDLL( lib_file , ctypes.RTLD_GLOBAL )

    def __init__(self , prototype , bind = True):
        super(ExVecstrPrototype , self).__init__( ExVecstrPrototype.lib , prototype , bind = bind)


class ExVecstr(BaseCClass):
    """
    Super thin wrapper around a std::vector<string>.
    """
    TYPE_NAME = "ex_vecstr"

    _alloc     = ExVecstrPrototype("void* ex_vecstr_alloc()", bind=False)
    _free      = ExVecstrPrototype("void  ex_vecstr_free(ex_vecstr)")
    _size      = ExVecstrPrototype("int   ex_vecstr_size(ex_vecstr)")
    _push_back = ExVecstrPrototype("void  ex_vecstr_push_back(ex_vecstr, char*)")
    _find      = ExVecstrPrototype("int   ex_vecstr_find(ex_vecstr, char*)")
    _at        = ExVecstrPrototype("char* ex_vecstr_at(ex_vecstr, int)")
    _insert    = ExVecstrPrototype("char* ex_vecstr_insert(ex_vecstr, char*, int)")


    def __init__(self):
        c_ptr = self._alloc()
        super(ExVecstr, self).__init__(c_ptr)

    def __len__(self):
        return self._size()

    def __contains__(self, elt):
        return self._find(elt) >= 0

    def __getitem__(self, idx):
        if idx > len(self):
            raise IndexError('list index %d out of range [0,%d)' % (idx, len(self)))
        return self._at(idx)

    def append(self, elt):
        self._push_back(elt)

    def __setitem__(self, elt, idx):
        if idx > len(self):
            self.append(elt)
        else:
            self._insert(elt, idx)

    def __iter__(self):
        idx = 0
        while idx < len(self):
            yield self[idx]
            idx += 1

    def __str__(self):
        content = ["'%s'" % elt for elt in self]
        return '[%s]' % (', '.join(content))

    def free(self):
        self._free()

vec = ExVecstr()
assert len(vec) == 0

strs = ["Xanadu", "Yahoo", "Zanaris"]

count = 0
for elt in strs:
    assert len(vec) == count
    count += 1
    vec.append(elt)
    assert len(vec) == count

assert len(vec) == len(strs)

for elt in strs:
    assert elt in vec

for i in range(len(strs)):
    assert vec[i] == strs[i]

print "All tests pass. len(vec) =", len(vec)
print "vec = ", vec

print "Adding new elt", "Dr. Flikka"
vec.append("Dr. Flikka")

print "All tests pass. len(vec) =", len(vec)
print "vec = ", vec
